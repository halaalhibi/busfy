"""
This Model is responsible for manageing the app runtime and scheduling how it works
"""

def get_current_istanbul_time():
    """
    This Function returns the current istanbul time.
    """
    pass

def is_in_commute_window(route, current_time) -> bool:
    """
    This function is responsible for checking if the route is in commute window, and that the buses are active.
    For example:
        Working days ["Mon", "Tue", "Wed", "Thu", "Fri"]
        Active hours from 6 until 00
    It takes a route and the current time to check and validate
    return True or False
    """
    pass


def has_any_active_route(profile, current_time) -> list:
    """
    List of configured routes and current time to check that this route is indeed active
    return a list containing active routes
    """
    pass


def init_scheduler(cycle_callback):
    pass

