# Contribution – Nada Hany Mahmoud Abdelati

**Student ID:** 2509115192
**GitHub:** nadahany2004-hub

## Files I worked on
- `core/geo.py`
- `notify/dedup.py`

## core/geo.py – Geographical calculations
This module turns GPS coordinates into distances and travel times that the rest of the system uses to decide when to notify the user.

- **`haversine_distance(lat1, lon1, lat2, lon2)`**: Calculates the real distance in meters between the bus and the stop using the Haversine formula (based on the Earth's radius of 6,371 km).
- **`estimate_eta_minutes(distance_meters, avg_speed_kmh=15.0)`**: Estimates how many minutes the bus needs to reach the stop, based on an average speed (default 15 km/h). Raises an error if the speed is zero or negative.
- **`is_approaching(distance_meters, threshold_meters)`**: Returns True when the bus is within the "approaching" distance (e.g. 1000 m).
- **`is_arrived(distance_meters, threshold_meters)`**: Returns True when the bus is within the "arrived" distance (e.g. 150 m).
- Added a quick self-test (`python -m core.geo`) that checks the functions with a real example (Taksim → Kadıköy).

## notify/dedup.py – Preventing duplicate notifications
This module makes sure the user never receives the same notification twice.

- **`build_dedup_key(event_type, route_name, bus_plate, date_str)`**: Builds a unique key for each notification by combining the event type, route, bus plate and date (e.g. `APPROACHING|Home-Work|34 ABC 123|2026-11-01`).
- **`is_already_sent(state, dedup_key)`**: Checks whether a notification with this key was already sent.
- **`mark_as_sent(state, dedup_key)`**: Saves the key in the shared state (`state["sent_notifications"]`) after sending, without adding duplicates.

## How it fits in the project
`geo.py` calculates how far the bus is and when it will arrive, and decides if it is approaching or has arrived. `dedup.py` then makes sure each of these alerts is sent only once per route, bus and day.
