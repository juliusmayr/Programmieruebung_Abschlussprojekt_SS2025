import streamlit as st
from datetime import date

st.title("Kalender")
selected_date = st.date_input("Wählen Sie ein Datum", value=date.today())
