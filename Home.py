import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Herzlich Willkommen in unserer Sport-App! 🏃‍♂️")
st.write("### Navigation")
column1, column2, column3 = st.columns(3)


with column1:
    st.page_link("pages/Athlet.py", label="🏃 Athlet")

with column2:
    st.page_link("pages/Trainingsauswertung.py", label="🗺️ Trainingsauswertung")

with column3:
    st.page_link("pages/Kalender.py", label="📅 Kalender")


