"""
This Module is Responsible for validating information.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from math import isfinite


ISTANBUL_TZ = ZoneInfo("Europe/Istanbul")

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
    if not isinstance(timestamp_str, str) or not timestamp_str.strip():
        return False

    try:
        # Parse IETT timestamp format: "2026-11-03 17:30:15"
        bus_time = datetime.strptime(timestamp_str.strip(),"%Y-%m-%d %H:%M:%S")
        bus_time = bus_time.replace(tzinfo=ISTANBUL_TZ)

        now = datetime.now(ISTANBUL_TZ)
        age_minutes = (now - bus_time).total_seconds() / 60.0

        return 0 <= age_minutes <= max_age_minutes
    except (ValueError, TypeError):
        return False


def parse_bus_record(raw_dict: dict) -> dict | None:
    """
    Validates and cleans a raw bus record from IETT's
    GetHatOtoKonum_json.
    Returns a clean dictionary with float coordinates, or None if
    invalid.
    """
    if not isinstance(raw_dict, dict):
        return None

    bus_id = raw_dict.get("kapino")
    line = raw_dict.get("hatkodu")
    lat_raw = raw_dict.get("enlem")
    lon_raw = raw_dict.get("boylam")
    direction = raw_dict.get("yon", "")
    timestamp = raw_dict.get("son_konum_zamani", "")
    nearest_stop = raw_dict.get("yakinDurakKodu")

    # Essential fields check
    if not bus_id or not line or lat_raw is None or lon_raw is None:
        return None

    # Coordinate validation
    if not is_valid_coordinate(lat_raw, lon_raw):
        return None

     # Timestamp freshness check (rejects ghost buses >15 min old)
    if timestamp and not is_timestamp_fresh(timestamp, max_age_minutes=15):
        return None

    return {
        "bus_id": str(bus_id).strip(),
        "line": str(line).strip(),
        "lat": float(lat_raw),
        "lon": float(lon_raw),
        "direction": str(direction).strip(),
        "timestamp": str(timestamp).strip(),
        "nearest_stop_code": str(nearest_stop) if nearest_stop else
        None,
    }