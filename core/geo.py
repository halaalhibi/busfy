"""
This Module is Responsible for Geographical calculations to change them into Standard measurement and time units
"""
import math

EARTH_RADIUS_M = 6_371_000


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Returns the distance in meters between the bus (lat1, lon1) and the stop (lat2, lon2)
    using the Haversine formula.
    """
    # 1) Convert degrees to radians (math.sin/cos only work with radians)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    # 2) Haversine formula
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 3) Angle * Earth's radius = distance in meters
    return EARTH_RADIUS_M * c


def estimate_eta_minutes(distance_meters: float, avg_speed_kmh: float = 15.0) -> float:
    """
    Returns the estimated time in minutes for a bus to cover the given distance.
    Example: 1000 m at 15 km/h -> 4.0 minutes
    """
    if avg_speed_kmh <= 0:
        raise ValueError("avg_speed_kmh must be positive")

    speed_m_per_min = avg_speed_kmh * 1000 / 60   # 15 km/h = 250 m/min
    return distance_meters / speed_m_per_min


def is_approaching(distance_meters: float, threshold_meters) -> bool:
    """
    Returns True if the bus is within the approaching distance (e.g. 1000 m).
    """
    return distance_meters <= threshold_meters


def is_arrived(distance_meters: float, threshold_meters) -> bool:
    """
    Returns True if the bus is within the arrived distance (e.g. 150 m).
    """
    return distance_meters <= threshold_meters


if __name__ == "__main__":
    # Quick test: run "python -m core.geo" from the project folder
    d = haversine_distance(41.0369, 28.9850, 40.9903, 29.0290)   # Taksim -> Kadikoy
    print(f"Distance: {d:.0f} m")
    print(f"ETA for 1000 m: {estimate_eta_minutes(1000):.1f} min")
    print("Approaching (800 m):", is_approaching(800, 1000))
    print("Arrived (800 m):", is_arrived(800, 150))