"""

"""

def build_dedup_key(event_type: str, route_name: str, bus_plate:   str, date_str: str) -> str :
    """
    This function is responsible for building the internal key for push notifications
     so we can decide if it has been sent or not.
    """
    pass

def is_already_sent(state: dict, dedup_key: str) -> bool:
    """
    This function is responsible for checking if a push notification is already sent or not to avoid duplicates messages
    """
    pass

def mark_as_sent(state: dict, dedup_key: str):
    """
    This function will mark  a message/key after it's being.
    """
    pass