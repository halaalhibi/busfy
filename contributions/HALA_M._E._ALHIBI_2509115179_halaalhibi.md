# My Contribution – Busfy Project

**Contributor:** Hala Alhibi

I contributed to the Busfy project by developing two Python modules: `core/detector.py` and `core/validator.py`.

## 1. Bus Detection (`core/detector.py`)

Implemented three main functions:

- **`classify_state()`**: Classifies buses as `FAR`, `APPROACHING`, or `ARRIVED` based on distance thresholds defined in `config.py`.
- **`should_trigger_leave_now()`**: Compares the estimated arrival time (ETA) with the user's walking time to determine when to leave.
- **`detect_events()`**:
  - Filters buses by line, direction, and stop ID.
  - Uses distance data or calculates geographic distance through `core.geo` when needed.
  - Validates distance and ETA values.
  - Compares current and previous bus states to generate `APPROACHING`, `ARRIVED`, and `LEAVE_NOW` events.
  - Tracks bus states and reduces repeated notifications.

## 2. Data Validation (`core/validator.py`)

Implemented three main functions:

- **`is_valid_coordinate()`**: Validates latitude and longitude, including numerical checks and predefined Istanbul coordinate ranges.
- **`is_timestamp_fresh()`**: Checks timestamp validity and freshness using UTC, with a default maximum age of 15 minutes.
- **`parse_bus_record()`**:
  - Extracts and standardizes bus data from supported IETT API field names.
  - Validates required information, including bus IDs, lines, and coordinates.
  - Processes optional fields such as direction, stop IDs, distance, ETA, and timestamps.
  - Handles missing or invalid inputs and returns `None` for invalid required data.

## 3. Error Handling and Integration

- Used `try/except`, type checking, and safe dictionary access to handle invalid data.
- Used `isfinite()` to reject invalid numerical values.
- Designed both modules to work with the project's configuration, geographic calculations, API data, and notification system.

## Summary

My contribution focused on implementing **six functions across two modules**, providing the core logic for bus data validation, state classification, and notification event detection.
