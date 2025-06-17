import streamlit as st
from PIL import Image
from classes_elias.person import Person
from classes_elias.ekgdata import EKGdata
from src.analyze_data import gpx_data, gpx_data_pydeck
from datetime import timedelta

if "selected" not in st.session_state:
    st.session_state.selected = "Home"

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")

# Personen laden
person_data = Person.load_person_data()
list_of_persons = Person.get_person_list(person_data)

st.session_state.selected_person = st.selectbox("Person auswählen", options = list_of_persons)
#Laden eines Bildes 
selected_person_data = Person.find_person_data_by_name(str(st.session_state.selected_person))
person_image = selected_person_data["picture_path"]
image = Image.open(person_image)
st.image(image, caption=st.session_state.selected_person)

#Laden des Alters für die augewählte Person 
person = Person(selected_person_data)
st.write(f"Alter: {person.calc_age()} Jahre")


# Laden der EKG-Daten für die ausgewählte Person und den ausgewählten Test

selected_person = st.session_state.selected_person
st.session_state.selected_ekg_test = st.selectbox("Wähle einen EKG-Test", options=["Bitte Wählen Sie einen Test aus"] + [ekg_test["id"] for ekg_test in person_data[Person.find_person_data_by_name(selected_person)["id"]-1]["ekg_tests"]])
if st.session_state.selected_ekg_test != "Bitte Wählen Sie einen Test aus":
    ekg_test = EKGdata.load_by_id(person_data, st.session_state.selected_ekg_test)
    ekg_data = EKGdata(ekg_test)
    ekg_data.plot_time_series()
    st.plotly_chart(ekg_data.fig)
    st.write(f"Testdatum: {ekg_test['date']}")
    #st.write (ekg_data.df.head())
    minutes =  (ekg_data.df["Zeit in ms"].max() - ekg_data.df["Zeit in ms"].min()) / 1000
    td = timedelta(minutes= minutes)  # Konvertiere ms zu Minuten
    st.write(f"Testdauer: {td} Minuten")


uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"])
gpx_data_pydeck(uploaded_file)


