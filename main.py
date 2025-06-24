import streamlit as st
from PIL import Image
from src.classes.person import Person
from src.classes.ekgdata import EKGdata
from src.analyze_data import gpx_data_pydeck, gpx_elevation_profile

from datetime import timedelta


if "selected" not in st.session_state:
    st.session_state.selected = "Home"

st.title("Das ist unsere erste App")
st.write("## Hier ist der Inhalt der App")
# Layout
col1, col2 = st.columns([1, 3])
with col1:
    
    # Personen laden
    persons_data = Person.load_person_data()
    list_of_persons = Person.get_person_list(persons_data)

    st.session_state.selected_person = st.selectbox("__Person auswählen__", options = list_of_persons)
    # Laden eines Bildes 
    selected_person_data = Person.find_person_data_by_name(str(st.session_state.selected_person))
    person = Person(selected_person_data)
    person_image = selected_person_data["picture_path"]
    image = Image.open(person_image)
    st.image(image, caption=st.session_state.selected_person) 
    
    #Laden des Alters für die augewählte Person 
    
    st.write(f"__Alter__: {person.calc_age()} Jahre")
    st.write(f"__Geburtsjahr__: {person.date_of_birth}")

    # Geschlecht der Person anzeigen
    st.write(f"__Geschlecht__: {person.gender}")

    subcol1, subcol2 = st.columns([1, 1])
    with subcol1:
        with st.popover(label = "✏️", help="Hier können Sie die Personendaten bearbeiten."): 
            person.edit_person(persons_data)
    with subcol2:
        with st.popover(label = ":heavy_plus_sign:", help="Hier können Sie eine neue Person hinzufügen."):
            st.write("Diese Funktion ist noch nicht implementiert.")
           




with col2:
    subcol1, subcol2, subcol3 = st.columns([2, 3, 1])
    with subcol2:
        st.write("__Info__")
    selected_person = st.session_state.selected_person
    with subcol1:
        st.session_state.selected_ekg_test = st.selectbox("__EKG-Test auswählen__", options=["Bitte Wählen Sie einen Test aus"] + person.get_ekg_test_list())

    with subcol3:
        with st.popover(label = ":bar_chart:", help = "Hier können Sie einen EKG-Test hinzufügen."):
            st.write("Diese Funktion ist noch nicht implementiert.")
    ekg_data_selected = EKGdata.load_by_id(persons_data, st.session_state.selected_ekg_test)
    if st.session_state.selected_ekg_test != "Bitte Wählen Sie einen Test aus":
        ekg_test = EKGdata.load_by_id(persons_data, st.session_state.selected_ekg_test)
        ekg_data = EKGdata(ekg_test)
        with subcol2:
            hours =  (ekg_data.df["Zeit in ms"].max() - ekg_data.df["Zeit in ms"].min()) / (1000*60**2)
            td = timedelta(hours=hours)  # Konvertiere ms zu Minuten
            total_seconds = td.total_seconds()
            #whole_hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            st.write(f"__Testdauer__: {minutes} Minuten")
            st.write(f"__Testdatum__: {ekg_test['date']}")
            heart_rate = ekg_data.estimate_heart_rate()
            st.write(f"__⌀ Herzfrequenz__: {heart_rate} [bpm]")
        
        ekg_data.fig = ekg_data.plot_time_series()
        st.plotly_chart(ekg_data.fig)
    
            
# Kartendarstellung der GPX-Daten

st.write("## Kartendarstellung der GPX-Daten")


uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"])

try:
    gpx_data_pydeck(uploaded_file)
    uploaded_file.seek(0)
    fig = gpx_elevation_profile(uploaded_file)
    #st.title("GPX Höhenprofil")
    st.plotly_chart(fig)
except:
    st.write("Bitte laden Sie eine GPX-Datei hoch, um die Kartendarstellung zu sehen.")