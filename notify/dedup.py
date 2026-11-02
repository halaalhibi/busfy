"""
This Module prevents sending the same notification twice.

Every notification gets a unique "key" (text). After sending it we save the key
inside state["sent_notifications"]. Before sending a new one we check if its key
is already there.
"""

SENT_KEY = "sent_notifications"


def build_dedup_key(event_type: str, route_name: str, bus_plate: str, date_str: str) -> str:
    """
    Builds a unique key for a notification.
    Example: build_dedup_key("APPROACHING", "Home-Work", "34 ABC 123", "2026-11-01")
             -> "APPROACHING|Home-Work|34 ABC 123|2026-11-01"
    """
    return f"{event_type}|{route_name}|{bus_plate}|{date_str}"


def is_already_sent(state: dict, dedup_key: str) -> bool:
    """
    Returns True if this notification was already sent, False otherwise.
    """
    return dedup_key in state.get(SENT_KEY, [])


def mark_as_sent(state: dict, dedup_key: str):
    """
    Saves the key in the state so we don't send the same notification again.
    """
    if SENT_KEY not in state:
        state[SENT_KEY] = []

    if dedup_key not in state[SENT_KEY]:
        state[SENT_KEY].append(dedup_key)