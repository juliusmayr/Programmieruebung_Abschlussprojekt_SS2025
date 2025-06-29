import json
from datetime import date
import streamlit as st
from PIL import Image
import os

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where the person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data
    

    @staticmethod
    def load_by_id(person_id):
        """
        A Function that knows where the persons id is.
        Returns a Dictionary with the Persons.
        """
        person_data = Person.load_person_data()
        for person in person_data: 
            if person_id == person["id"]:
                return person_data[person_id-1]  # IDs in JSON sind 1-basiert, Python-Listen sind 0-basiert
        return {'None'}
            
    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list of all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
        
    @staticmethod
    def add_person(persons_data):
        """
        A Function that adds a new person to the persons json file.
        """
        st.write("Neue Person hinzufügen")
        with st.form("person_form_add"):
            id = len(persons_data) + 1
            firstname = st.text_input("Vorname")
            lastname = st.text_input("Nachname")
            date_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=date.today().year, step=1)
            gender = st.selectbox("Geschlecht", options=["male","female", "diverse"])
            picture = st.file_uploader("Bild hochladen", type=["jpg", "jpeg"])
            submitted = st.form_submit_button("Hinzufügen")

        if submitted:
            if not firstname or not lastname:
                st.warning("Bitte geben Sie Vor- und Nachnamen ein.")
                return
            if picture:
                picture_path = f"data/pictures/{id}.jpg"
                img = Image.open(picture)
                img.save(picture_path, format="JPEG")
            else:
                picture_path = "data/pictures/default.jpg"
            
            new_person = {
                "id": id,
                "firstname": firstname,
                "lastname": lastname,
                "date_of_birth": int(date_of_birth),
                "gender": gender,
                "picture_path": picture_path,
                "ekg_tests": []
            }
            persons_data.append(new_person)
            with open("data/person_db.json", "w") as file:
                json.dump(persons_data, file, indent=4)
            st.success("Neue Person hinzugefügt!")

    @staticmethod
    def delete_person(persons_data, person_id):
        """
        Eine Funktion, die eine Person anhand der ID aus der JSON-Datei löscht und vergibt neue IDs.
        """
        
        new_persons_data = [p for p in persons_data if p["id"] != person_id] # IDs werden neu vergeben
        for idx, person in enumerate(new_persons_data, start=1):
            person["id"] = idx
        #Speicher
        with open("data/person_db.json", "w") as file:
            json.dump(new_persons_data, file, indent=4)
        # Bild löschen
        picture_path = f"data/pictures/{person_id}.jpg"
        if os.path.exists(picture_path):
            os.remove(picture_path)
        

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"] if "picture_path" in person_dict else "data/pictures/default.jpg"
        self.id = person_dict["id"]
        self.gender = person_dict["gender"]

    def get_ekg_test_list(self):
        """ 
        A Function that returns a list of all EKG tests available for the person.
        """
        data = Person.load_by_id(self.id)
        if "ekg_tests" in data:
            ekg_tests = []
            for ekg_test in data["ekg_tests"]:
                ekg_tests.append(ekg_test["id"])
            return ekg_tests
    
    def calc_age(self):
        """
        A Function that calculates the age of a person based on the date of birth
        """
        today = date.today()
        age = today.year - int(self.date_of_birth)
        return age

    def calc_max_heart_rate(self):
        """
        A Function that calculates the Persons maximum Heart Rate based on the age.
        """
        age = self.calc_age()
        max_heart_rate = 220 - age
        return max_heart_rate
    
    def edit_person(self, persons_data):
        """
        A Function that edits person json file.
        """
        st.write("Personendaten bearbeiten")
        with st.form("person_form_edit"):
            self.id = int(st.text_input("ID", value=str(self.id), disabled=True))
            self.firstname = st.text_input("Vorname", value=self.firstname)
            self.lastname = st.text_input("Nachname", value=self.lastname)
            self.date_of_birth = st.number_input("Geburtsjahr", value=int(self.date_of_birth), min_value=1900, max_value=date.today().year, step=1)
            self.gender = st.selectbox("Geschlecht", options=["male", "female", "diverse"], index=["male", "female", "diverse"].index(self.gender))
            picture = st.file_uploader("Bild hochladen", type=["jpg", "jpeg"])
            img = Image.open(picture) if picture else Image.open(self.picture_path)
            img.save(self.picture_path, format="JPEG")
            submitted = st.form_submit_button("Speichern")

        if submitted:
            for person in persons_data:
                
                if str(person["id"]) == str(self.id):
                    
                    person["id"] = self.id
                    person["date_of_birth"] = self.date_of_birth
                    person["firstname"] = self.firstname
                    person["lastname"] = self.lastname
                    person["gender"] = self.gender
                    person["picture_path"] = self.picture_path
                    person["ekg_tests"] = person["ekg_tests"]
                    break
            save_path = "data/person_db.json"
        
            with open(save_path, "w") as file:
                json.dump(persons_data, file, indent=4)
            st.success("Personendaten aktualisiert!")
            


        

if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))
    print(Person.load_by_id(1))
    person = Person(Person.load_by_id(1))
    print(person.calc_age())
    print(person.calc_max_heart_rate())