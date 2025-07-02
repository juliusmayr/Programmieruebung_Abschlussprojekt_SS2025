import streamlit as st
from src.analyze_data import gpx_data_pydeck, gpx_elevation_profile

st.set_page_config(
    page_title="GPX",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("🗺️ Karte")
    st.markdown("Willkommen im Karten-Bereich!")

st.title("GPX-Datenanalyse")
uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"])

try:
    gpx_data_pydeck(uploaded_file)
    uploaded_file.seek(0)
    fig = gpx_elevation_profile(uploaded_file)
    #st.title("GPX Höhenprofil")
    st.plotly_chart(fig)
except:
    st.write("Bitte laden Sie eine GPX-Datei hoch, um die Kartendarstellung zu sehen.")