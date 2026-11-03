"""
This Module is the entry point for our app
"""
import config
import schedule
import notify.channel as channel
import notify.dedup as dedup
import notify.rules as rules
import core.detector as detector
import core.validator as validator
import json
from dotenv import load_dotenv
import os
from pathlib import Path
from api import iett_client
import time

load_dotenv()

INTERVAL = 60
NOTIFY_CHANNEL = os.getenv("NOTIFY_CHANNEL")


def load_profile() -> dict:
    """Loads user settings from data/profile.json safely."""
    path = Path(config.PROFILE_PATH)
    if path.exists() and path.stat().st_size > 0:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user": "student", "ntfy_topic": NOTIFY_CHANNEL, "routes": []}


def load_state() -> dict:
    """Loads runtime state from data/state.json safely."""
    path = Path(config.STATE_PATH)
    if path.exists() and path.stat().st_size > 0:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "HOURLY_REQUESTS": 0,
        "RATE_LIMIT_HOUR": 0,
        "bus_states": {},
        "sent_notifications": []
    }

def save_state(state: dict):
    """Saves updated state back to data/state.json."""
    path = Path(config.STATE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def run_monitoring_cycle(profile: dict, state: dict):
    """
    The main Loop that will:
        Read Profile
        Check if we're in commute windows
        Get live Buses
        Calculate Distance
        Detects Change
        Sends Notifcations
        update state.json
    of course the logic isn't just this
    """
    current_time = schedule.get_current_istanbul_time()
    time_str = current_time.strftime("%H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")

    active_routes = schedule.has_any_active_route(profile, current_time)
    if not active_routes:
        print("No active routes Waiting....")
        return
    topic = profile.get("ntfy_topic")

    for route in active_routes:
        route_name = route.get("name")
        line_code = route.get("line")
        enabled_alerts = route.get("alerts", ["approaching", "leave_now", "arrived", "disruption"] )

        print(f"Checking Bus on line {line_code}")
        raw_busses = iett_client.fetch_buses_for_line(line_code, state)
        validated_buses = []
        if raw_busses is not None and len(raw_busses) > 0:
            for raw_bus in raw_busses:
                validated_bus = validator.parse_bus_record(raw_bus)
                if validated_bus is not None:
                    validated_buses.append(validated_bus)
                if not validated_buses:
                    print("No active Buses Found at the moment")
                    continue
        events = detector.detect_events(validated_buses , route, state )
        for event in events:
            event_type = event.get("type").lower()
            if event_type not in enabled_alerts:
                continue
            bus_id = event.get("bus_id")
            debup_key = dedup.build_dedup_key(event_type, route_name,bus_id, date_str)
            if dedup.is_already_sent(state, debup_key):
                continue

            if event_type == "approaching":
                title, msg, priority = rules.format_approaching_message(
                    event["bus"], route,
                    event["distance_meters"], event["eta_minutes"]
                )
            elif event_type == "leave_now":
                walk_min = route.get("walk_minutes", 6)
                title, msg, priority =rules.format_leave_now_message(
                    event["bus"], route, walk_min,
                    event["eta_minutes"]
                )
            elif event_type == "arrived":
                title, msg, priority = rules.format_arrived_message(event["bus"], route)
            else:
                continue
            print(f"[{time_str}] Triggering {event_type.upper()}  alert: {title} ")
            success = channel.send_ntfy_push(topic , title, msg, priority)
            if success:
                dedup.mark_as_sent(state, debup_key)

        if "disruption" in enabled_alerts:
            announcements = iett_client.fetch_announcements(state)
            for announcement in announcements:
                if announcement.get("HATKODU") == line_code:
                    announcement_id = announcement.get("GUNCELLEME_SAATI", date_str)
                    disrupt_key =dedup.build_dedup_key("disruption",
                                                       route_name,line_code, announcement_id)
                    if not dedup.is_already_sent(state, disrupt_key):
                        title,msg,priority = rules.format_disruption_message(announcement, route)
                        print(f"[{time_str}] Sending DISRUPTION alert for {line_code}")
                        success = channel.send_ntfy_push(topic,title, msg, priority)
                        if success:
                            dedup.mark_as_sent(state, disrupt_key)
    save_state(state)

def main():
    """
    The main Setup, probably while true loop.
    """
    print("Starting Busfy....")
    state = load_state()

    while True:
        try:
            profile = load_profile()
            run_monitoring_cycle(profile, state)
        except Exception as e:
            print(f"Some error happened {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()