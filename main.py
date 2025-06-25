import streamlit as st
from PIL import Image
from src.classes.person import Person
from src.classes.ekgdata import EKGdata
from src.analyze_data import gpx_data_pydeck, gpx_elevation_profile
from datetime import date
from datetime import timedelta

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")
