"""
This module is responsible for detecting changes for any alerts
It acts as our state machine.
"""

from config import ARRIVED_DISTANCE_METERS, APPROACHING_DISTANCE_METERS
from core.geo import haversine_distance
from math import isfinite

def classify_state(distance_meters: float) -> str:
    """
    This Function is responsible for classifying the state of the bus from meters to string such as
    "APPROACHING"
    """

    if distance_meters <= ARRIVED_DISTANCE_METERS:
        return "ARRIVED"
    elif distance_meters <= APPROACHING_DISTANCE_METERS:
        return "APPROACHING"
    else:
        return "FAR"


def should_trigger_leave_now(eta_minutes: float, walk_minutes: int) -> bool:
   """
   This function returns weather to leave now or not based on  walk_minutes to the bus station
   """
    
    if eta_minutes <= walk_minutes:
        return True
    else:
        return False

def detect_events(current_buses: list[dict], route: dict, state: dict) -> list[dict]:
    """
    This function is responsible for detecting events based on current buses and route
    It acts as the main state machine.
    """

    events = []
    bus_states = state.setdefault("bus_states", {})

    for bus in current_buses:

        if route.get("line") is not None:
            if bus.get("line") != route["line"]:
                continue

        if route.get("direction") is not None:
            if bus.get("direction") != route["direction"]:
                continue

        if route.get("stop_id") is not None:
            stop_ids = bus.get("stop_ids")

            if not isinstance(stop_ids, (list, tuple, set)):
                continue

            if str(route["stop_id"]) not in [str(s) for s in stop_ids]:
                continue

        bus_id = bus.get("bus_id")
        line = bus.get("line")

        if not bus_id or line is None:
            continue

        bus_id = str(bus_id)

        distance_meters = bus.get("distance_meters")

        if distance_meters is None:
            coordinates = (
                bus.get("lat"),
                bus.get("lon"),
                route.get("stop_lat"),
                route.get("stop_lon")
            )

            if any(value is None for value in coordinates):
                continue

            try:
                distance_meters = haversine_distance(
                    *(float(value) for value in coordinates)
                )
            except (TypeError, ValueError, OverflowError):
                continue

        try:
            distance_meters = float(distance_meters)
        except (TypeError, ValueError, OverflowError):
            continue

        if not isfinite(distance_meters) or distance_meters < 0:
            continue

        bus_state = classify_state(distance_meters)

        previous = bus_states.get(bus_id, {})
        previous_state = previous.get("status")

        if previous_state is not None:

            if bus_state == "APPROACHING" and previous_state == "FAR":
                events.append({
                    "type": "APPROACHING",
                    "line": line,
                    "bus_id": bus_id
                })

            if bus_state == "ARRIVED" and previous_state != "ARRIVED":
                events.append({
                    "type": "ARRIVED",
                    "line": line,
                    "bus_id": bus_id
                })

        eta_minutes = bus.get("eta_minutes")
        walk_minutes = route.get("walk_minutes")
        leave_now = False

        if eta_minutes is not None and walk_minutes is not None:
            try:
                eta_minutes = float(eta_minutes)
                walk_minutes = float(walk_minutes)

                if (
                    isfinite(eta_minutes)
                    and isfinite(walk_minutes)
                    and eta_minutes >= 0
                    and walk_minutes >= 0
                ):
                    leave_now = should_trigger_leave_now(
                        eta_minutes,
                        walk_minutes
                    )

            except (TypeError, ValueError, OverflowError):
                pass

        already_alerted = previous.get("leave_now_sent", False)

        if leave_now and not already_alerted:
            events.append({
                "type": "LEAVE_NOW",
                "line": line,
                "bus_id": bus_id
            })

        bus_states[bus_id] = {
            "status": bus_state,
            "leave_now_sent": (
                (leave_now or already_alerted)
                if bus_state != "FAR"
                else False
            )
        }

    return events


