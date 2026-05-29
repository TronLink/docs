#!/usr/bin/env python3
"""Verify the 7 inline JSON Schema mirrors in mcp-server-tronlink.{en,zh}.md
stay in parity with upstream Zod schemas in tronlink-mcp-core.

What it checks (top-level fields only — nested object shapes are out of scope):

1. Every top-level field in the upstream Zod `z.object({...})` is present in
   the doc's `properties`.
2. No doc property is absent from the upstream Zod schema.
3. `required` parity: a field is required upstream iff it is required in the
   doc (i.e. has no `.optional()` in Zod and is listed in `required` in JSON).

Run locally:
    python3 scripts/check_doc_schema_parity.py

Pin the upstream SHA via env (recommended for CI reproducibility):
    SCHEMAS_PIN=<sha>  python3 scripts/check_doc_schema_parity.py

Exit codes:
    0  parity holds
    1  drift detected (one or more tools mismatch)
    2  fetch / parse error (network failure, missing schema, malformed doc)
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Tools we mirror inline. Doc heading → upstream Zod schema name.
MIRRORED_TOOLS: dict[str, str] = {
    "tl_chain_send": "chain_send",
    "tl_chain_swap_v3": "chain_swap_v3",
    "tl_chain_stake": "chain_stake",
    "tl_multisig_submit_tx": "multisig_submit_tx",
    "tl_gasfree_send": "gasfree_send",
    "tl_chain_get_account": "chain_get_account",
    "tl_evaluate": "evaluate",
}

REPO = Path(__file__).resolve().parent.parent
DOC_PATHS: tuple[Path, ...] = (
    REPO / "docs/ai-support/mcp-server-tronlink.en.md",
    REPO / "docs/ai-support/mcp-server-tronlink.zh.md",
)

DEFAULT_PIN = "main"
UPSTREAM_TEMPLATE = (
    "https://raw.githubusercontent.com/TronLink/tronlink-mcp-core/{ref}/"
    "src/mcp-server/schemas.ts"
)


# ── Upstream fetch ──────────────────────────────────────────────────────────


def fetch_upstream(ref: str) -> str:
    url = UPSTREAM_TEMPLATE.format(ref=ref)
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"FETCH FAILED ({e.code}): {url}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"FETCH FAILED ({e.reason}): {url}") from e


# ── Zod schema parsing ─────────────────────────────────────────────────────


def extract_zod_body(source: str, schema_name: str) -> str:
    """Return the inside of `<schema_name>: z.object({ ... })` via brace matching."""
    pattern = re.compile(rf"\b{re.escape(schema_name)}:\s*z\.object\(\s*\{{")
    m = pattern.search(source)
    if not m:
        raise ValueError(f"Zod schema {schema_name!r} not found in upstream source")
    start = m.end()  # right after opening `{`
    depth = 1
    i = start
    while i < len(source) and depth > 0:
        c = source[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    if depth != 0:
        raise ValueError(f"Unbalanced braces in Zod schema {schema_name!r}")
    return source[start : i - 1]


def _chain_has_top_optional(chain: str) -> bool:
    """True iff `.optional()` appears at brace-depth 0 of the chain.

    A nested `.optional()` (inside `z.object({ ... .optional() ... })`) belongs
    to a nested field, not to the outer one — we only care about the outermost.
    """
    depth = 0
    i = 0
    while i < len(chain):
        c = chain[i]
        if c == "{":
            depth += 1
            i += 1
        elif c == "}":
            depth -= 1
            i += 1
        elif depth == 0 and chain.startswith(".optional()", i):
            return True
        else:
            i += 1
    return False


def parse_zod_top_level(body: str) -> dict[str, bool]:
    """Return {field_name: is_required}. Top-level fields are 4-space indented."""
    out: dict[str, bool] = {}
    current_name: str | None = None
    current_chain: list[str] = []

    def commit() -> None:
        if current_name is None:
            return
        joined = " ".join(current_chain)
        out[current_name] = not _chain_has_top_optional(joined)

    # Top-level field: 4-space indent, then `field_name: z` (z may be alone on
    # the line with .method() chained on continuation lines).
    top_re = re.compile(r"^    ([a-zA-Z_][a-zA-Z0-9_]*):\s*(z(?:\..*)?)$")
    cont_re = re.compile(r"^      ")  # 6+ spaces = continuation of current field
    for line in body.split("\n"):
        m = top_re.match(line)
        if m:
            commit()
            current_name = m.group(1)
            current_chain = [m.group(2)]
            continue
        if current_name is not None and cont_re.match(line):
            current_chain.append(line.strip())
    commit()
    return out


# ── Doc JSON Schema parsing ────────────────────────────────────────────────


HEADING_RE = re.compile(r"####\s+`(tl_[a-z0-9_]+)`")
JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def parse_doc_schemas(doc_text: str) -> dict[str, dict[str, bool]]:
    """For every `#### `tl_xxx`` heading followed by a ```json block,
    return {tool: {field: is_required}}.
    """
    results: dict[str, dict[str, bool]] = {}
    for heading in HEADING_RE.finditer(doc_text):
        tool = heading.group(1)
        # Search for the next ```json block after this heading
        after = doc_text[heading.end():]
        # Stop at the next heading of equal-or-higher level
        next_heading = re.search(r"\n(#{1,4})\s", after)
        scope = after[: next_heading.start()] if next_heading else after
        jm = JSON_BLOCK_RE.search(scope)
        if not jm:
            continue
        try:
            schema = json.loads(jm.group(1))
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON for {tool}: {e}") from e
        if not isinstance(schema, dict):
            continue
        props = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        results[tool] = {name: (name in required) for name in props.keys()}
    return results


# ── Diff ───────────────────────────────────────────────────────────────────


def diff_tool(
    tool: str,
    zod: dict[str, bool],
    doc: dict[str, bool],
) -> list[str]:
    """Return a list of human-readable drift messages (empty if in parity)."""
    msgs: list[str] = []
    missing_in_doc = sorted(set(zod) - set(doc))
    extra_in_doc = sorted(set(doc) - set(zod))
    common = set(zod) & set(doc)
    req_drift = sorted(f for f in common if zod[f] != doc[f])
    if missing_in_doc:
        msgs.append(f"  fields in upstream Zod but missing from doc: {missing_in_doc}")
    if extra_in_doc:
        msgs.append(f"  fields in doc but not in upstream Zod: {extra_in_doc}")
    for f in req_drift:
        zod_state = "required" if zod[f] else "optional"
        doc_state = "required" if doc[f] else "optional"
        msgs.append(f"  required/optional mismatch on {f!r}: upstream={zod_state}, doc={doc_state}")
    return msgs


# ── Main ───────────────────────────────────────────────────────────────────


def main() -> int:
    ref = os.environ.get("SCHEMAS_PIN", DEFAULT_PIN)
    print(f"Fetching upstream schemas.ts at {ref}")
    source = fetch_upstream(ref)
    print(f"  {len(source):,} bytes")

    # Parse upstream once
    zod_by_tool: dict[str, dict[str, bool]] = {}
    for tool, zod_name in MIRRORED_TOOLS.items():
        try:
            body = extract_zod_body(source, zod_name)
            zod_by_tool[tool] = parse_zod_top_level(body)
        except ValueError as e:
            print(f"PARSE FAILED: {e}", file=sys.stderr)
            return 2

    # Diff against each doc
    any_failure = False
    for doc_path in DOC_PATHS:
        if not doc_path.exists():
            print(f"DOC MISSING: {doc_path}", file=sys.stderr)
            return 2
        text = doc_path.read_text(encoding="utf-8")
        try:
            doc_by_tool = parse_doc_schemas(text)
        except ValueError as e:
            print(f"DOC PARSE FAILED ({doc_path.name}): {e}", file=sys.stderr)
            return 2

        rel = doc_path.relative_to(REPO)
        for tool in MIRRORED_TOOLS:
            if tool not in doc_by_tool:
                print(f"FAIL {rel}::{tool}")
                print(f"  doc has no inline JSON Schema block for this tool")
                any_failure = True
                continue
            drifts = diff_tool(tool, zod_by_tool[tool], doc_by_tool[tool])
            if drifts:
                print(f"FAIL {rel}::{tool}")
                for d in drifts:
                    print(d)
                any_failure = True
            else:
                print(f"  OK  {rel}::{tool}")

    if any_failure:
        print()
        print("Doc/upstream parity check FAILED.")
        print("Either update the inline JSON Schema blocks to match upstream,")
        print("or pin SCHEMAS_PIN to a known-good commit if upstream is mid-flight.")
        return 1

    print()
    print(f"OK: {len(MIRRORED_TOOLS)} tools × {len(DOC_PATHS)} docs in parity with upstream {ref}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
