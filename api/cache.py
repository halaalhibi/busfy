import os
from pathlib import Path
import iett_client
import time

REFRESH_INTERVAL = 30

def ensure_lines(path, state):
    if not os.path.exists(path):
        Path(path).touch()
    mtime = Path(path).stat().st_mtime
    now = int((time.time() - mtime) / 86400)
    if now > REFRESH_INTERVAL or Path(path).stat().st_size == 0:
        data = iett_client.fetch_all_lines(state)
        if data:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(data)

def ensure_stops(path,state):
    if not os.path.exists(path):
        Path(path).touch()
    mtime = Path(path).stat().st_mtime
    now = int((time.time() - mtime) / 86400)
    if now > REFRESH_INTERVAL or Path(path).stat().st_size == 0:
        data = iett_client.fetch_all_stops(state)
        # print(f"{data} d")
        if data:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(data)


if __name__ == "__main__":
    ensure_stops(str("/home/lotekk/Coding/Python/busfy/data/stops.json"), {})
    ensure_lines(str("/home/lotekk/Coding/Python/busfy/data/lines.json"), {})
