import streamlit as st
from PIL import Image
from src.classes.person import Person
from src.classes.ekgdata import EKGdata
from src.analyze_data import gpx_data_pydeck, gpx_elevation_profile
from datetime import date
from datetime import timedelta

st.title("Herzlich Willkommen in unserer Sport-App! 🏃‍♂️")
st.write("### Navigation")
column1, column2, column3 = st.columns(3)


with column1:
    st.page_link("pages/Athlet.py", label="🏃 Athlet")

with column2:
    st.page_link("pages/Karte.py", label="🗺️ Karte")

with column3:
    st.page_link("pages/Kalender.py", label="📅 Kalender")


