import json
import pandas as pd
import plotly.express as px

from src.classes.person import Person

class EKGdata:
    """
    Diese Klasse liest EKG-Daten aus einer CSV-Datei ein und bietet Funktionen zur Analyse der Daten.
    Sie kann Peaks im EKG-Signal finden, die Herzfrequenz schätzen und die Daten visualisieren.
    Die EKG-Daten werden in einem DataFrame gespeichert, der die Messwerte in mV und die Zeit in ms enthält.
    Die Klasse kann auch EKG-Tests anhand einer ID laden.
    """
## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält

    @staticmethod
    def load_by_id(input_persons, test_id):
        """
        Diese Funktion lädt den EKG-Test anhand der ID und der Personen-Datenbank.
        """
        input_persons = Person.load_person_data()
        for person in input_persons:
            for ekg_test in person["ekg_tests"]:
                if ekg_test["id"] == test_id:
                    return ekg_test
    
    def find_peaks(self, threshold=340):
        """
        a function that finds R-peaks in an EKG signal.
        """

        list_of_peaks = []	

        for index, row in self.df.iterrows():   
            if index == self.df.index.max():
                break 

            current_value = row['Messwerte in mV']

            # ist der current_value größer als der Vorgänger und Nachfolger
            if current_value > self.df.iloc[index-1]["Messwerte in mV"] and current_value >= self.df.iloc[index+1]["Messwerte in mV"]:
                #print("Found a peak at index: ", index)
                if current_value > threshold:
                    list_of_peaks.append(index)
        return list_of_peaks

    def plot_time_series(self, threshold=340):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        list_of_peaks = self.find_peaks(threshold)
        self.df["is_peak"] = False
        self.df.loc[list_of_peaks, "is_peak"] = True

        self.fig = px.line(self.df.head(5000), x="Zeit in ms", y="Messwerte in mV", title='EKG Data with Peaks Highlighted')
        self.fig.add_scatter(x= self.df.iloc[self.find_peaks(threshold)]['Zeit in ms'], 
                    y=self.df.loc[self.df["is_peak"], 'Messwerte in mV'], 
                    mode='markers', 
                    marker=dict(color='red', size=5), 
                    name='Peaks')
        return self.fig 

    def estimate_heart_rate(self, threshold=340):
        """
        Diese Funktion schätzt die Herzfrequenz basierend auf den gefundenen Peaks.
        """
        list_of_peaks = self.find_peaks(threshold)
        if len(list_of_peaks) < 2:
            return None
        # Berechne die Zeitdifferenz zwischen den Peaks
        peak_intervals = [self.df.iloc[list_of_peaks[i+1]]['Zeit in ms'] - self.df.iloc[list_of_peaks[i]]['Zeit in ms'] for i in range(len(list_of_peaks)-1)]
        # Berechne die durchschnittliche Zeitdifferenz
        average_interval = sum(peak_intervals) / len(peak_intervals)
        # Berechne die Herzfrequenz in bpm (Beats per Minute)
        heart_rate = 60000 / average_interval if average_interval > 0 else None
        return heart_rate

if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())

    test_ekg = EKGdata(ekg_dict)
    print("Estimated Heart Rate:", test_ekg.estimate_heart_rate(), "[BPM]")
    test_ekg.plot_time_series().show(renderer="browser")
    # test_ekg.estimate_heart_rate()
    
