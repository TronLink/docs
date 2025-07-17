# Asset Filter Logic Documentation

## Overview
This document describes the implementation of asset filtering logic in the TronLink wallet, specifically focusing on the interaction between basic mode, security anti-fraud reminder mode, and asset display settings.

## Core Components

### 1. Filter States
- `hideLittleAssets`: Controls whether to hide small value assets
- `hideScamToken`: Controls whether to hide scam tokens

### 2. Mode States
- `isBasicMode`: Indicates if the wallet is in basic mode
- `isAntiCheatOpen`: Indicates if security anti-fraud reminder is enabled

## Implementation Details

### Filter Status Management

#### Reading Filter Status
The `readHideLittleAssetsFlag()` method handles the initialization and updates of filter states:
1. Retrieves saved filter settings from storage
2. Gets current mode status
3. Updates filter states based on mode status
4. Updates UI to reflect current filter states

#### Filter State Updates
The `updateFiltersState()` method manages filter state logic:
1. In basic mode:
   - Forces `hideLittleAssets` to false
   - Ignores saved small assets hiding setting
2. In non-basic mode:
   - Uses saved `hideLittleAssets` setting
3. For scam token filtering:
   - Only applies when anti-fraud reminder is enabled
   - Uses saved `hideScamToken` setting

### Mode Change Handling

#### Basic Mode Changes
When basic mode is enabled:
1. Switches to user-defined sorting if currently using value-based sorting
2. Updates filter states
3. Refreshes UI

#### Anti-Fraud Mode Changes
When anti-fraud reminder is disabled:
1. Clears saved scam token hiding setting
2. Updates filter states
3. Refreshes UI

### UI Updates
The `updateFiltersUI()` method:
1. Updates filter indicators in the UI
2. Reflects current filter states to users

## Key Methods

### `readHideLittleAssetsFlag()`
- Purpose: Initialize and update filter states
- Trigger: Mode changes, app startup
- Dependencies: Saved settings, current mode status

### `updateFiltersState()`
- Purpose: Apply filter logic based on mode
- Parameters:
  - `isBasicMode`: Basic mode status
  - `isAntiCheatOpen`: Anti-fraud reminder status
  - `savedHideLittleAssets`: Saved small assets hiding setting
  - `savedHideScamToken`: Saved scam token hiding setting

### `handleBasicModeChanged()`
- Purpose: Handle basic mode state changes
- Actions:
  - Updates sorting if needed
  - Refreshes filter states

### `handleAntiCheatChanged()`
- Purpose: Handle anti-fraud reminder state changes
- Actions:
  - Clears scam token settings if disabled
  - Updates filter states

## State Dependencies

1. Basic Mode Impact:
   - Overrides small assets hiding setting
   - Forces user-defined sorting

2. Anti-Fraud Reminder Impact:
   - Controls scam token filtering
   - Clears settings when disabled

## UI Integration

The filter states are reflected in the UI through:
1. Filter indicators
2. Asset list display
3. Sorting options

## Future Considerations

1. Potential improvements:
   - Add more granular filter controls
   - Implement filter presets
   - Add filter statistics

2. Maintenance points:
   - Monitor filter performance
   - Track user filter preferences
   - Optimize filter update frequency 