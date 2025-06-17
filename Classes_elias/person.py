import json
from datetime import datetime, date

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data
    

    @staticmethod
    def load_by_id(person_id):
        """A Function that knows where te persons ID is returns a Dictionary with the Persons"""
        person_data = Person.load_person_data()
        for person in person_data: 
            if person_id == person["id"]:
                return person_data[person_id-1] 
        return {'None'}
            
    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
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
        
        
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.gender = person_dict["gender"]

    def calc_age(self):
        """A Function that calculates the age of a person based on the date of birth"""
        #date_of_birth = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - int(self.date_of_birth)
        return age

    def calc_max_heart_rate(self):
        """A Function that calculates the Persons maximum Heart Rate based on the age"""
        age = self.calc_age()
        max_heart_rate = 220 - age
        return max_heart_rate
        

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