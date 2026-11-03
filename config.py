"""
This Module Contains Constants Variables and File Paths
"""
from pathlib import Path

# File Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROFILE_PATH = "data/profile.json"
STATE_PATH = "data/state.json"
STOPS_PATH = "data/stops.json"
LINES_PATH = "data/lines.json"

#Threshold
#TODO: Make a correct threshold that don't make the person who's using this app curse you
APPROACHING_DISTANCE_METERS = 1000
ARRIVED_DISTANCE_METERS = 150
HOURLY_API_BUDGET = 95

def ensure_directories():
    """
    This Function Checks for the Data directory to ensure existing, if not, creates it.
    """
    try:
        (SCRIPT_DIR / "data").mkdir(parents=True, exist_ok=True)
        if not (SCRIPT_DIR / PROFILE_PATH).exists():
            return False
        if not (SCRIPT_DIR / STATE_PATH).exists():
            return False
        if not (SCRIPT_DIR / LINES_PATH).exists():
            return False
        if not (SCRIPT_DIR / STOPS_PATH).exists():
            return False
    except FileExistsError:
        return False
    return True