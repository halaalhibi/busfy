"""
This Module is the entry point for our app
"""
import config
import schedule
import notify.channel as channel
import notify.dedup as dedup
import notify.rules as rules
import core.detector as detector
import core.geo as geo
import core.validator as validator
import json
from dotenv import load_dotenv
import os


load_dotenv()

INTERVAL = 60
NOTIFY_CHANNEL = os.getenv("NOTIFY_CHANNEL")

def load_profile() -> dict:
    with open(config.PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state() -> dict:
    with open(config.STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

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
    pass


def main():
    """
    The main Setup, probably while true loop.
    """
    pass

if __name__ == "__main__":
    main()