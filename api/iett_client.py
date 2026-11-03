"""
This Module is Responsible for Communicating over the IETT API.
There's a note that the IETT API
"""
import zeep
import json
import api.wsdl_cleaner as wsdl_cleaner
from datetime import datetime
from zoneinfo import ZoneInfo

ISTANBUL_TZ = ZoneInfo("Europe/Istanbul")

clients = {}

def connect_client(service_name: str, timeout: int = 20) -> zeep.Client:
    """
    This function will connect to the IETT API, and return a handle for that
    """
    if service_name not in clients:
        transport = zeep.Transport(timeout=timeout, operation_timeout=timeout)
        wsdl_path = wsdl_cleaner.get_wsdl(service_name)
        clients[service_name] = zeep.Client(str(wsdl_path), transport=transport)
    return clients[service_name]


def send_request(service: str, operation: str, retries: int = 2, **kwargs) -> str:
    """
    this function will send a SOAP  request to the IETT API, and will retrieve the response.
    it returns the aqquired info from the IETT API
    """
    tried = 0
    while tried < retries:
        try:
            client = connect_client(service)
            method = getattr(client.service, operation)
            response = method(**kwargs)
            return response
        except Exception as e:
            tried += 1
            print(e)
    return ""


def can_make_request(state, max_rate=95) -> bool:
    """
    Checks if we are within the hourly budget. Resets counter
    each new hour.
    """
    current_hour = datetime.now(ISTANBUL_TZ).hour
    last_hour = state.get("RATE_LIMIT_HOUR")

    if last_hour != current_hour:
        state["RATE_LIMIT_HOUR"] = current_hour
        state["HOURLY_REQUESTS"] = 0

    return state.get("HOURLY_REQUESTS", 0) < max_rate


def record_request(state):
    """
    This function will add the request counter in our state dictionary after every request that have been made.
    """
    state["HOURLY_REQUESTS"] = state.get("HOURLY_REQUESTS", 0) + 1


def fetch_buses_for_line(line_code: str, state: dict) -> list[dict]:
    """
    This function will take the bus number and the state dictionary and it'll
        Check if it can make request
        it make request to GetHatOtoKonum_json endpoint from IETT API
        record that request
    the returned Request is in this format:
    {
        "kapino": "B-1872",
        "boylam": "28.99263",
        "enlem": "41.10806",
        "hatkodu": "50H",
        "guzergahkodu": "50H_D_D0",
        "hatad": "ALİBEYKÖY - HACIOSMAN METRO",
        "yon": "ALİBEYKÖY METRO",
        "son_konum_zamani": "2026-10-29 22:44:57",
        "yakinDurakKodu": "115191"
    }
    This function will be the function that helps us track the bus location.
    """
    if can_make_request(state):
        response = send_request("Live_Vehicle","GetHatOtoKonum_json" ,HatKodu=line_code)
        record_request(state)
        if not response:
            return []
        return json.loads(response)
    return []


def fetch_all_stops(state) -> str:
    """
    this function will get all the stops available in the IETT API from GetDurak_csv endpoint.
    it'll return a csv text containing all the stops available in the IETT API
    """
    if can_make_request(state):
        response = send_request("Schedule","GetDurak_json", DurakKodu="")
        record_request(state)
        if not  response:
            return ""
        return response
    return ""

def fetch_all_lines(state) -> str:
    """
    this function will get all the lines available in the IETT API from GetHat_csv endpoint.
    it'll return a csv text containing all the lines available in the IETT API
    """
    if can_make_request(state):
        response = send_request("Schedule","GetHat_json", HatKodu="")
        record_request(state)
        if not  response:
            return ""
        return response
    return ""

def fetch_announcements(state) -> list[dict]:
    """
    Get all announcements from the IETT API, from GetDuyurular_json endpoint.
    the returned Request is in this format:
    {
        "HATKODU": "41E",
        "HAT": "AYAZAGA - KABATAS",
        "TIP": "Günlük",
        "GUNCELLEME_SAATI": "Kayit Saati: 09:12",
        "MESAJ": "GÜZERGAHTAKI YOGUN TRAFIK NEDENIYLE ARAÇLARIMIZ AYAZAGA KALKISLI SEFERLERINE 20 DAKIKA VE ÜZERI RÖTARLI HAREKET ETMEKTEDIR.\t"
    }
    """
    if can_make_request(state):
        response = send_request("Announcement","GetDuyurular_json" )
        record_request(state)
        if not response:
            return []
        return json.loads(response)
    return []



"""
Some TODO's in future:
    add Fetch_planned seferler.
"""