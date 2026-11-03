"""
This Module is Responsible for validating information.
"""

from datetime import datetime, timezone
from math import isfinite

def is_valid_coordinate(lat: float, lon: float) -> bool:
    """
    checks that the coming coordinates are within Istanbul
        Latitude: 40.5 to 41.6,
        Longitude: 28.0 to 30.0
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError, OverflowError):
        return False

    return (
        isfinite(lat)
        and isfinite(lon)
        and 40.5 <= lat <= 41.6
        and 28.0 <= lon <= 30.0
    )

def is_timestamp_fresh(timestamp_str:str , max_age_minutes = 15) -> bool:
    """
    ensures that the given information aren't old, this ensures no wrong info are sent to the user
    """
    try:
        max_age_minutes = float(max_age_minutes)

        if not isfinite(max_age_minutes) or max_age_minutes < 0:
            return False

        if not isinstance(timestamp_str, str):
            return False

        timestamp_str = timestamp_str.strip()

        if not timestamp_str:
            return False

        timestamp = datetime.fromisoformat(
            timestamp_str.replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            return False

        now = datetime.now(timezone.utc)
        age_minutes = (
            now - timestamp.astimezone(timezone.utc)
        ).total_seconds() / 60

        return 0 <= age_minutes <= max_age_minutes

    except (TypeError, ValueError, OverflowError):
        return False

def parse_bus_record(raw_dict: dict) -> dict | None:
    """
    To validate any corrupted response from the IETT API
    """
    if not isinstance(raw_dict, dict):
        return None

    def get_value(*keys):
        for key in keys:
            value = raw_dict.get(key)
            if value is not None and value != "":
                return value
        return None

    bus_id = get_value("bus_id", "kapino", "kapiNo", "vehicle_id")
    line = get_value("line", "hatkodu", "hatKodu")
    direction = get_value("direction", "yon", "yön")

    lat = get_value("lat", "enlem", "latitude")
    lon = get_value("lon", "boylam", "longitude")

    if bus_id is None or line is None:
        return None

    if not is_valid_coordinate(lat, lon):
        return None

    bus_id = str(bus_id).strip()
    line = str(line).strip()

    if not bus_id or not line:
        return None

    result = {
        "bus_id": bus_id,
        "line": line,
        "lat": float(lat),
        "lon": float(lon)
    }

    if direction is not None:
        result["direction"] = str(direction).strip()

    stop_ids = get_value("stop_ids")

    if isinstance(stop_ids, (list, tuple, set)):
        result["stop_ids"] = [str(s) for s in stop_ids]

    distance = get_value("distance_meters")

    if distance is not None:
        try:
            distance = float(distance)

            if isfinite(distance) and distance >= 0:
                result["distance_meters"] = distance

        except (TypeError, ValueError, OverflowError):
            pass

    eta = get_value("eta_minutes")

    if eta is not None:
        try:
            eta = float(eta)

            if isfinite(eta) and eta >= 0:
                result["eta_minutes"] = eta

        except (TypeError, ValueError, OverflowError):
            pass

    timestamp = get_value("timestamp", "timestamp_str")

    if timestamp is not None:
        if not is_timestamp_fresh(timestamp):
            return None

        result["timestamp"] = timestamp

    return result
