import streamlit as st
from PIL import Image

from src.classes.person import Person
from src.classes.ekgdata import EKGdata
from src.analyze_data import gpx_data, gpx_data_pydeck
import os
from datetime import timedelta
from streamlit.components.v1 import html

if "selected" not in st.session_state:
    st.session_state.selected = "Home"

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")

# Personen laden
persons_data = Person.load_person_data()
list_of_persons = Person.get_person_list(persons_data)

st.session_state.selected_person = st.selectbox("Person auswählen", options = list_of_persons)
#Laden eines Bildes 
selected_person_data = Person.find_person_data_by_name(str(st.session_state.selected_person))
person_image = selected_person_data["picture_path"]
image = Image.open(person_image)
st.image(image, caption=st.session_state.selected_person)

#Laden des Alters für die augewählte Person 
person = Person(selected_person_data)
st.write(f"Alter: {person.calc_age()} Jahre, Geburtsjahr: {person.date_of_birth}")

# Geschlecht der Person anzeigen
st.write(f"Geschlecht: {person.gender}")


# Laden der EKG-Daten für die ausgewählte Person und den ausgewählten Test


with st.expander(label = "Bearbeiten", icon = "✏️", expanded = False):
    person.edit_person(persons_data)
    

selected_person = st.session_state.selected_person
st.session_state.selected_ekg_test = st.selectbox("EKG-Test auswählen", options=["Bitte Wählen Sie einen Test aus"] + person.get_ekg_test_list())
if st.session_state.selected_ekg_test != "Bitte Wählen Sie einen Test aus":
    ekg_test = EKGdata.load_by_id(persons_data, st.session_state.selected_ekg_test)
    ekg_data = EKGdata(ekg_test)
    st.write(f"### EKG-Test ID: {ekg_data.id}")
    ekg_data.fig = ekg_data.plot_time_series()
    st.plotly_chart(ekg_data.fig)
    st.write(f"Testdatum: {ekg_test['date']}")
    #st.write (ekg_data.df.head())
    minutes =  (ekg_data.df["Zeit in ms"].max() - ekg_data.df["Zeit in ms"].min()) / 1000
    td = timedelta(minutes= minutes)  # Konvertiere ms zu Minuten
    st.write(f"Testdauer: {td} Minuten")

st.write("## Kartendarstellung der GPX-Daten")


uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"])

try:
    gpx_data_pydeck(uploaded_file)
except:
    st.write("Bitte laden Sie eine GPX-Datei hoch, um die Kartendarstellung zu sehen.")
