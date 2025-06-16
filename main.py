import streamlit as st
import gpxpy
import plotly.express as px
import pandas as pd
import json
from src.analyze_data import gpx_data, gpx_data_pydeck, gpx_to_geojson

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

# Beispiel-Daten
# GPX-Datei hochladen
#uploaded_file = st.file_uploader("Bitte GPX-Datei hinzufügen", type="gpx")
uploaded_file = st.file_uploader("Bitte GPX-Datei hinzufügen", type="gpx")
fig = gpx_data_pydeck(uploaded_file)


