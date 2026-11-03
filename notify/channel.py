"""
This Module is responsible for sending push notification to the client
"""
import requests

def send_ntfy_push(topic: str, title: str, message: str, priority: str = "default") -> bool:
    """
    Sends a push notification to ntfy.sh.
    Returns True on HTTP 200 success, False otherwise.
    """
    if not topic:
        return False
    url = f"https://ntfy.sh/{topic.strip()}"
    headers = {
        "Title": title,
        "Priority": priority,
    }

    try:
        response = requests.post(
            url,
            data=message.encode("utf-8"),
            headers=headers,
            timeout=10,
        )
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error sending ntfy push: {e}")
        return False

