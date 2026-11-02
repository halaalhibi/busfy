"""
This Module is responsible for building our web page
Don't panic No HTML/CSS/Javascript
instead Streamlit python Library that handles those for us
i don't know how this library work but we will learn
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import config
from notify.channel import send_ntfy_push



@st.cache_data
def load_stops_data():
    with open(config.STOPS_PATH, encoding="utf-8") as f:
        stops_data = json.load(f)
    df = pd.DataFrame(stops_data)
    return df

def load_lines_data():
    with open(config.LINES_PATH, encoding="utf-8") as f:
        lines_data = json.load(f)
    df = pd.DataFrame(lines_data)
    return df

def render_header():
    st.title("Busfy Configuration")
    st.caption("Don't miss your bus again")

def render_stop_search(stops_df):
    query = st.text_input(
        "Search your stop",
        placeholder="Stop name, district, or stop code (e.g. Sarıyer, 100022)",
        key="stop_query",
    ).strip()

    if not query:
        st.info("Type a stop name, district or code to search.")
        return None


def render_line_selector():
    pass

def render_commute_window_picker():
    pass

def render_test_notification_button(ntfy_topic: str) :
    pass

def save_profile(profile_data: dict):
    pass


def load_profile():
    pass

if __name__ == "__main__":
    render_header()
    df = load_stops_data()
