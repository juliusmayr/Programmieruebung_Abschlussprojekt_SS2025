# Abschlussprojekt Progammierübung 2
## Anwendung
Um dieses Projekt starten zu können muss nach dem Klonen des Repositories der Befehl `pdm install` ausgeführt werden. Um die Streamlit-App zu öffnen muss der Befehl `streamlit run main.py` ausgeführt werden, wenn ein Fehler angezeigt wird `pdm run streamlit` ausführen.
## Funktionen der App
Beim starten der App wird man auf die Seite 'Home' geleitet, die Auswahlmöglichkeiten sind Athlet, Kalender, Trainingsauswertung. Bei Anwahl des Athlet Felds wird man weitergeleitet. Es erscheint ein Dropdownmenü zur Personenauswhl. Personen können bearbeitet, hinzugefügt und gelöscht werden. Bei Auswahl einer Person erscheint das Dropdownmenü zur Auswahl verschiedener EKG Tests, beim auswählen wird dieser angezeigt. Es können ebenfalls neue EKG Tests hinzugefügt werden.

Bei Anwahl von Kalender, wird ein Kalender gezeigt indem Trainingsdaten sowie EKG Daten sichtbar werden. 

Bei Anwahl von Trainingsauswertung, öffnet sich eine neue Seite, das Dropdownmenü dient zur Wahl der Person, für diese eine Trainingseinheit angezeigt werden soll. Sind unter dieser Person schon Daten(GPX,Fit-Files) gespeichert werden diese angezeigt, fall noch keine Daten vorliegen, können diese hochgeladen werden. Zum einen wird eine Kartendarstellung erstellt, auf der die asolvierte Trainingseinheit erscheint (z.B.: gefahrene/ gelaufene Sttrecke). Dazu wird ein Höhenprofil erstellt, was darunter angezeigt wird.
Die Fit-Files, werden von der App in CSV-Dateien umgewandelt, wodurch sie dargestellt werden können, es können ebenfalls neue Fit-Files gedownloadet werden. Es erscheint ein Dropdownmenü mit der Auswahl welche Spalte der Fit-File in Abhängigkeit zur Zeit geplottet werden soll, die ausgewählte Funktion wird geplottet und angezeigt.

Gespeicherte Daten bleiben auch bei Schließen der App erhalten.

Um die App bedienen zu können exestiert eine Navigationsleiste.