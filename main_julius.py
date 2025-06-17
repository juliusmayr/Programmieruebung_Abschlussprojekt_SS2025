import streamlit as st
from src.analyze_data import gpx_data, gpx_data_pydeck
from classes_julius.person import Person
from PIL import Image


if "selected" not in st.session_state:
    st.session_state.selected = "Home"

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")

# Personen laden
person_data = Person.load_person_data()
list_of_persons = Person.get_person_list(person_data)

st.session_state.selected_person = st.selectbox("Person auswählen", options = list_of_persons)
st.write(st.session_state.selected_person)

#Laden eines Bildes 
selected_person_data = Person.find_person_data_by_name(str(st.session_state.selected_person))
person_image = selected_person_data["picture_path"]
image = Image.open(person_image)
st.image(image, caption=st.session_state.selected_person)

#Laden des Alters für die augewählte Person 
person = Person(selected_person_data)
st.write(f"Alter:{person.calc_age()}Jahre")


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


