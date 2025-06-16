import streamlit as st
import gpxpy
import plotly.express as px
import pandas as pd

from src.analyze_data import gpx_data, gpx_data_pydeck

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
uploaded_file = st.file_uploader("Bitte GPX-Datei hinzufügen", type="gpx")
fig = gpx_data_pydeck(uploaded_file)

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# st.plotly_chart(fig)

