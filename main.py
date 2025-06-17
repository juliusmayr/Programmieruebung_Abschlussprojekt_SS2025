import streamlit as st

import plotly.express as px
import pandas as pd
import json
from src.analyze_data import gpx_data, gpx_data_pydeck
import time

if "selected" not in st.session_state:
    st.session_state.selected = "Home"

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")

# Sidebar
st.sidebar.title("Navigation")

# Navigation
st.sidebar.radio(
    "Wähle eine Seite",
    ["Home", "Analyse", "Visualisierung"],
    key="selected"
)

uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"])
gpx_data_pydeck(uploaded_file)


