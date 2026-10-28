"""
This module is responsible for detecting changes for any alerts
It acts as our state machine.
"""

def classify_state(distance_meters: float) -> str:
    """
    This Function is responsible for classifying the state of the bus from meters to string such as
    "APPROACHING"
    """

def should_trigger_leave_now(eta_minutes: float, walk_minutes: int) -> bool:
   """
   This function returns weather to leave now or not based on  walk_minutes to the bus station
   """
   pass


def detect_events(current_buses: list[dict], route: dict, state: dict) -> list[dict]:
    """
    This function is responsible for detecting events based on current buses and route
    It acts as the main state machine.
    """
    pass



