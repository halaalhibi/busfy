"""
This Module is the entry point for our app
"""
INTERVAL = 60

def load_profile() -> dict:
    pass

def load_state() -> dict:
    pass

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