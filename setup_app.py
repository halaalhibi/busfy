"""
This Module is responsible for building our web page
Don't panic No HTML/CSS/Javascript
instead Streamlit python Library that handles those for us
i don't know how this library work but we will learn
AI here were used to help implement this streamlit app
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import config
from notify.channel import send_ntfy_push




def parse_wkt_point(wkt_str: str) -> tuple[float, float]:
    """Extracts (lat, lon) from 'POINT (lon lat)' format."""
    clean = wkt_str.replace("POINT (", "").replace(")", "").strip()
    lon_str, lat_str = clean.split()
    return float(lat_str), float(lon_str)

def normalize_text(text: str) -> str:
    # 1. Turn to lowercase string
    clean_text = str(text).lower()

    # 2. Swap each Turkish letter for an English letter
    clean_text = clean_text.replace("ç", "c")
    clean_text = clean_text.replace("ğ", "g")
    clean_text = clean_text.replace("ı", "i")
    clean_text = clean_text.replace("i̇", "i")
    clean_text = clean_text.replace("ö", "o")
    clean_text = clean_text.replace("ş", "s")
    clean_text = clean_text.replace("ü", "u")

    return clean_text

@st.cache_data
def load_stops_data():
    with open(config.STOPS_PATH, encoding="utf-8") as f:
        stops_data = json.load(f)
    df = pd.DataFrame(stops_data)
    #Add this for normalization
    combined = (df["SDURAKADI"].astype(str) + " "
                + df["ILCEADI"].astype(str) + " "
                + df["SDURAKKODU"].astype(str)
    )
    df["SEARCH_TEXT"] = combined.apply(normalize_text)
    return df

@st.cache_data
def load_lines_data():
    with open(config.LINES_PATH, encoding="utf-8") as f:
        lines_data = json.load(f)
    df = pd.DataFrame(lines_data)
    return df

def save_profile(profile_data: dict):
    profile_path = Path(config.PROFILE_PATH)
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)


def load_profile() -> dict:
    profile_path = Path(config.PROFILE_PATH)
    if profile_path.exists() and profile_path.stat().st_size > 0:
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user": "student", "ntfy_topic": "busfy-alerts",
            "routes": []}

def render_header():
    st.title("Busfy Configuration")

def render_stop_search(stops_df):
    """
    this is the search engine for our app.
    it creates a search box, searches via SDURAKADI, ILCEADI, SDURAKKODU, and will show only the first 20 matches.
    it'll format the result to avoid confusion
    """
    # to get the desired user from data
    query = st.text_input(
        "Search your stop",
        placeholder="Stop name, district, or stop code (e.g. Sarıyer, 100022)",
        key="stop_query",
    ).strip()
    if not query:
        st.info("Type a stop name, district or code to search.")
        return None

    clean_query = normalize_text(query)
    matching_rows = stops_df["SEARCH_TEXT"].str.contains(clean_query,na = False)
    results = stops_df[matching_rows].head(20)

    if results.empty:
        st.warning("No stops found matching your search.")
        return None

    # Format stop choices for selectbox, for calirfying
    stop_labels = []
    for index, row in results.iterrows():
        label = f"{row['SDURAKADI']} ({row['ILCEADI']}) - Code:{row['SDURAKKODU']}"
        stop_labels.append(label)

    # take the input from the selected box
    selected_label = st.selectbox("Select your stop",options=stop_labels)
    selected_idx = stop_labels.index(selected_label)
    selected_row = results.iloc[selected_idx]

    lat, lon = parse_wkt_point(str(selected_row["KOORDINAT"]))

    return {
        "id": int(selected_row["SDURAKKODU"]),
        "name": str(selected_row["SDURAKADI"]),
        "district": str(selected_row["ILCEADI"]),
        "lat": lat,
        "lon": lon,
    }


def render_line_selector(lines_df):
    st.subheader("Bus Line")

    # 1. Build a clean list of line labels
    line_labels = []
    for index, row in lines_df.iterrows():
        label = f"{row['SHATKODU']} - {row['SHATADI']}"
        line_labels.append(label)

        # 2. Dropdown (user can type to search)
    selected_option = st.selectbox("Select Bus Line",options=line_labels)

    # 3. Extract just the line code (e.g. "79E" from "79E -KAYABAŞI...")
    line_code = selected_option.split(" - ")[0]
    return line_code


def render_commute_window_picker() -> dict:
    st.subheader("Commute Timing & Preferences")

    # 1. Days of the week (st.multiselect allows picking multipleoptions)
    all_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    selected_days = st.multiselect("Active Days",options = all_days,default = ["Mon", "Tue", "Wed", "Thu", "Fri"])

    # 2. Start and End hours
    col1, col2 = st.columns(2)
    with col1:
        start_hour = st.number_input("Start Hour (0 to 23)", min_value = 0, max_value = 23, value = 7)
    with col2:
        end_hour = st.number_input("End Hour (0 to 23)", min_value = 0, max_value = 23, value = 9)

    # 3. Walking time to the stop
    walk_minutes = st.number_input("Walking time to stop (minutes)", min_value = 1, max_value = 60, value = 6)

    # 4. Alerts to enable
    available_alerts = ["approaching", "leave_now", "arrived","disruption"]
    selected_alerts = st.multiselect("Enabled Alerts",options = available_alerts,   default = available_alerts)

    return {
        "working_days": selected_days,
        "start_hour": int(start_hour),
        "end_hour": int(end_hour),
        "walk_minutes": int(walk_minutes),
        "alerts": selected_alerts,
    }


def render_test_notification_button(ntfy_topic: str) -> str:
    st.subheader("Notification Settings")

    # 1. Text input for topic name
    topic = st.text_input( "ntfy.sh Topic Name", value=ntfy_topic,
        help="Subscribe to this topic name inside your ntfy mobileapp.").strip()

    # 2. Test button
    if st.button("Send Test Push Notification"):
        if not topic:
            st.error("Please enter a topic name first.")
        else:
            success = send_ntfy_push(topic=topic,title="Busfy Test Alert",
            message="Notifications are working! You are ready for your commute.",
            priority="default"
            )
            if success:
                st.success(f"Notification sent! Check your phone ontopic: {topic}")
            else:
                st.warning("Sent request, but make surenotify / channel.py is implemented!")
    return topic




def main():
    render_header()

    # 1. Load cached stops, lines, and user profile
    stops_df = load_stops_data()
    lines_df = load_lines_data()
    profile = load_profile()

    # 2. Notification Topic Settings
    current_topic = profile.get("ntfy_topic", "busfy-alerts")
    new_topic = render_test_notification_button(current_topic)
    if new_topic != current_topic:
        profile["ntfy_topic"] = new_topic
        save_profile(profile)

    st.divider()

    # 3. Add a New Route Form
    st.header("➕ Add a Commute Route")
    route_name = st.text_input(
        "Route Name",
        placeholder="e.g. Morning to Campus",
        key="new_route_name"
    ).strip()

    selected_stop = render_stop_search(stops_df)
    selected_line = render_line_selector(lines_df)
    timing_settings = render_commute_window_picker()

    if st.button("💾 Save Route"):
        if not route_name:
            st.error("Please give your route a name (e.g. 'Morningto Campus').")
        elif not selected_stop:
            st.error("Please search and select a bus stop.")
        else:
            # Combine stop, line, and timing into a single routedictionary
            new_route = {
                "name": route_name,
                "line": selected_line,
                "stop": selected_stop,
                "working_days": timing_settings["working_days"],
                "start_hour": timing_settings["start_hour"],
                "end_hour": timing_settings["end_hour"],
                "walk_minutes": timing_settings["walk_minutes"],
                "alerts": timing_settings["alerts"],
            }
            profile["routes"].append(new_route)
            save_profile(profile)
            st.success(f"Route '{route_name}' saved successfully!")
            st.rerun()
        st.divider()

        # 4. View and Manage Existing Routes
        st.header("📋 Your Configured Routes")
        saved_routes = profile.get("routes", [])

        if not saved_routes:
            st.info("No routes added yet. Use the form above to add your first route!")
        else:
            for index, route in enumerate(saved_routes):
                with st.expander(f"{route['name']} (Line: {route['line']})", expanded=True):
                    col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Stop:** {route['stop']['name']} ({route['stop']['district']})")
                st.write(f"**Stop Code:** `{route['stop']['id']}` ")
                st.write(f"**Walk Time:** {route['walk_minutes']} minutes")
            with col2:
                days_str = ", ".join(route["working_days"])
                st.write(f"**Days:** {days_str}")
                st.write(f"**Hours:** {route['start_hour']: 02d}: 00 to {route['end_hour']: 02d}: 00 ")
                st.write(f"**Active Alerts:** {''.join(route['alerts'])}")

             # Delete button with a unique key per route
            if st.button("Delete Route",key=f"delete_route_{index}"):
                profile["routes"].pop(index)
                save_profile(profile)
                st.rerun()

if __name__ == "__main__":
    main()
