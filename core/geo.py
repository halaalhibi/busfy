"""
This Module is Responsible for Geographical calculations to change them into Standard measurement and time units
"""

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    MATH !!!!!
    Uses the standard Haversine formula with Earth's radius (R = 6, 371, 000 m)
    to calculate the real geographic distance across Earth's surface.
    it takes latitude and longitude as input and returns distance in meters.
    the latitude and longitude 1 are for the bus while 2 is for the station
    """
    pass


def estimate_eta_minutes(distance_meters: float,avg_speed_kmh: float = 15.0) -> float:
    """
    this function takes distance in meters and estimated city bus speed
    and returns the estimated times in minutes.
    """
    pass

def is_approaching(distance_meters: float, threshold_meters) -> bool:
    """
    this function returns weather a bus is approaching or note depending on it's destance and a comparing constant
    """
    pass

def is_arrived(distance_meters: float, threshold_meters) -> bool:
    """
    this function returns weather a bus is arrived or not
    """
    pass
