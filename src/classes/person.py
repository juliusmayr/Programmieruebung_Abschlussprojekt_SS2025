import json
from datetime import date
import streamlit as st
from PIL import Image
import os
from tinydb import TinyDB, Query

class Person:
    db_path = "data/person_db.json"

    @staticmethod
    def get_db():
        return TinyDB(Person.db_path)

    @staticmethod
    def load_person_data():
        db = Person.get_db()
        data = db.all()
        db.close()
        return data

    @staticmethod
    def load_by_id(person_id):
        db = Person.get_db()
        result = db.search(Query().id == person_id)
        db.close()
        if result:
            return result[0]
        return {}

    @staticmethod
    def get_person_list(person_data):
        return [f'{eintrag["lastname"]}, {eintrag["firstname"]}' for eintrag in person_data]

    @staticmethod
    def find_person_data_by_name(suchstring):
        if suchstring == "None":
            return {}
        try:
            nachname, vorname = suchstring.split(", ")
        except Exception:
            return {}
        db = Person.get_db()
        result = db.search((Query().lastname == nachname) & (Query().firstname == vorname))
        db.close()
        if result:
            return result[0]
        return {}

    @staticmethod
    def add_person(persons_data):
        st.write("Neue Person hinzufügen")
        with st.form("person_form_add"):
            db = Person.get_db()
            all_persons = db.all()
            used_ids = set(p["id"] for p in all_persons)
            # Finde die kleinste freie ID
            id = 1
            while id in used_ids:
                id += 1
            firstname = st.text_input("Vorname")
            lastname = st.text_input("Nachname")
            date_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=date.today().year, step=1)
            gender = st.selectbox("Geschlecht", options=["male","female", "diverse"])
            picture = st.file_uploader("Bild hochladen", type=["jpg", "jpeg"])
            submitted = st.form_submit_button("Hinzufügen")
        if submitted:
            if not firstname or not lastname:
                st.warning("Bitte geben Sie Vor- und Nachnamen ein.")
                db.close()
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
            db.insert(new_person)
            db.close()
            st.success("Person erfolgreich hinzugefügt!")
            

    @staticmethod
    def delete_person(persons_data, person_id):
        db = Person.get_db()
        # Vor dem Löschen: EKG-Dateien entfernen
        person = db.search(Query().id == person_id)
        if person and "ekg_tests" in person[0]:
            for ekg in person[0]["ekg_tests"]:
                ekg_path = ekg.get("result_link")
                if ekg_path and os.path.exists(ekg_path):
                    os.remove(ekg_path)
        db.remove(Query().id == person_id)
        # IDs NICHT mehr neu vergeben, sondern Lücken lassen
        db.close()
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
        data = Person.load_by_id(self.id)
        if "ekg_tests" in data:
            return [ekg_test["id"] for ekg_test in data["ekg_tests"]]

    def calc_age(self):
        today = date.today()
        age = today.year - int(self.date_of_birth)
        return age

    def calc_max_heart_rate(self):
        age = self.calc_age()
        max_heart_rate = 220 - age
        return max_heart_rate

    def edit_person(self, persons_data):
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
            db = Person.get_db()
            db.update({
                "firstname": self.firstname,
                "lastname": self.lastname,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender,
                "picture_path": self.picture_path
            }, Query().id == self.id)
            db.close()
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