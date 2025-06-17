import json
import pandas as pd
import plotly.graph_objects as go
import neurokit2 as nk
import numpy as np

from src.classes.person import Person

class EKGdata:
    """
    This class reads ECG data from a CSV file and provides functions for data analysis.
    It can detect peaks in the ECG signal, estimate heart rate, and visualize the data.
    The ECG data is stored in a DataFrame containing the measurements in mV and the time in ms.
    The class can also load ECG tests using an ID.
    """
## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.df = self.df.iloc[:5000] # Begrenze die Daten auf die ersten 5000 Zeilen für die Analyse
        self.df_to_numpy = self.df["Messwerte in mV"].to_numpy()  # Konvertiere die Messwerte in mV zu einem Numpy-Array
        #self.ecg_filtered = nk.signal_filter(self.df_to_numpy, lowcut=0.5, highcut=40, sampling_rate=100)
        self.signals, self.info = nk.ecg_process(self.df_to_numpy, sampling_rate=700, method = "neurokit") # Verarbeite die EKG-Daten mit NeuroKit2
    
    @staticmethod
    def load_by_id(input_persons, test_id):
        """
        This function loads the ECG test using the ID and the person database.
        """
        input_persons = Person.load_person_data()
        for person in input_persons:
            for ekg_test in person["ekg_tests"]:
                if ekg_test["id"] == test_id:
                    return ekg_test
    
    def find_peaks(self):
        """
        a function that finds R-peaks and T-peaks in an EKG signal.
        """
        self.r_peaks = self.info["ECG_R_Peaks"]
        self.t_peaks = self.info["ECG_T_Peaks"]

        return self.r_peaks, self.t_peaks

    def plot_time_series(self):
        """
        This function creates a time series visualization of the ECG signal with R- and T-peaks.
        It uses Plotly to visualize the ECG data.
        """
        # R- und T-Peaks extrahieren und bereinigen
        self.r_peaks = self.info["ECG_R_Peaks"]
        self.r_peaks = np.array(self.r_peaks)  # Konvertiere zu Numpy-Array
        self.r_peaks = self.r_peaks[~np.isnan(self.r_peaks)].astype(int)

        self.t_peaks = self.info["ECG_T_Peaks"]
        self.t_peaks = np.array(self.t_peaks)
        self.t_peaks = self.t_peaks[~np.isnan(self.t_peaks)].astype(int)
        # self.r_peaks, self.t_peaks = self.find_peaks()
        # self.r_peaks = self.r_peaks[~np.isnan(self.r_peaks)]
        # self.t_peaks = self.t_peaks[~np.isnan(self.t_peaks)] # R- und T-Peaks finden
        self.fig = go.Figure()

        x_part = self.df["Zeit in ms"] / 1000
        y_part = self.df["Messwerte in mV"]
        
        # EKG-Kurve
        self.fig.add_trace(go.Scatter(
            x=x_part,  # Zeit in Sekunden
            y=y_part,
            mode='lines',
            name='ECG',
            line=dict(color='blue'),
            showlegend=True
        ))

        # R-Peaks (grün, Marker mit "R")
        self.fig.add_trace(go.Scatter(
            x= x_part[self.r_peaks],
            y= y_part[self.r_peaks],
            mode='text',
            text=["R"] * len(self.r_peaks),
            textfont=dict(color='#006400', size=25),
            name='R-Peaks',
            showlegend=True
        ))

        # T-Peaks (rot, Marker mit "T")
        self.fig.add_trace(go.Scatter(
            x=x_part[self.t_peaks],
            y=y_part[self.t_peaks],
            mode='text',
            text=["T"] * len(self.t_peaks),
            textfont=dict(color='#8B0000', size=25),
            name='T-Peaks',
            showlegend=True))
        

        self.fig.update_layout(
            xaxis_title="t / [s]",
            yaxis_title="ECG / [mV]",
            template="simple_white"
        )

        return self.fig

    def estimate_heart_rate(self):
        """
        This function estimates the heart rate based on the ECG_Rate signal.
        """
        heart_rate = self.signals["ECG_Rate"].mean()  # Durchschnittliche Herzfrequenz in bpm
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
    
