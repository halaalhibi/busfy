"""
This Module Contains Constants Variables and File Paths
"""
# File Paths
PROFILE_PATH = "data/profile.json"
STATE_PATH = "data/state.json"
# STOPS_PATH = "data/stops.csv"
# LINES_PATH = "data/lines.csv"

#Threshold
APPROACHING_DISTANCE_METERS = 1000
ARRIVED_DISTANCE_METERS = 150
HOURLY_API_BUDGET = 95

def ensure_directories():
    """
    This Function Checks for the Data directory to ensure existing, if not, creates it.
    """
    pass