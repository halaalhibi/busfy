from datetime import datetime
from zoneinfo import ZoneInfo
import time

def get_current_istanbul_time():
    istanbul_time = datetime.now(ZoneInfo("Europe/Istanbul"))
    return istanbul_time

def is_in_commute_window(route, current_time) -> bool:
    day = current_time.strftime("%a")
    working_days = route["working_days"]

    if day not in working_days:
        return False

    start_hour = route["start_hour"]
    end_hour = route["end_hour"]
    hour = current_time.hour

    if end_hour == 0:
        return hour >= start_hour

    return start_hour <= hour < end_hour


def has_any_active_route(profile, current_time) -> list:
    active_routes = []

    for route in profile["routes"]:
        if is_in_commute_window(route, current_time):
            active_routes.append(route)

    return active_routes


def init_scheduler(cycle_callback):
    while True:
     cycle_callback()
     time.sleep(60)

 