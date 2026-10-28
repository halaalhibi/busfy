"""
This Module is Responsible for validating information.
"""

def is_valid_coordinate(lat: float, lon: float) -> bool:
    """
    checks that the coming coordinates are within Istanbul
        Latitude: 40.5 to 41.6,
        Longitude: 28.0 to 30.0
    """
    pass

def is_timestamp_fresh(timestamp_str:str , max_age_minutes = 15) -> bool:
    """
    ensures that the given information aren't old, this ensures no wrong info are sent to the user
    """
    pass

def parse_bus_record(raw_dict: dict) -> dict | None:
    """
    To validate any corrupted response from the IETT API
    """
    pass