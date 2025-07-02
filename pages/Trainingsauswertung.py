import streamlit as st
from src.analyze_data import gpx_data_pydeck, gpx_elevation_profile, fit_to_csv
import json

st.set_page_config(
    page_title="Trainingsauswertung",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Athletenauswahl ganz oben ---
persons_data = None
list_of_persons = None
options = None
try:
    from src.classes.person import Person
    persons_data = Person.load_person_data()
    list_of_persons = Person.get_person_list(persons_data)
    options = ["Person auswählen"] + list_of_persons
except Exception:
    options = ["Person auswählen"]
if "selected_person" not in st.session_state:
    st.session_state.selected_person = options[0]
selected_index = options.index(st.session_state.selected_person) if st.session_state.selected_person in options else 0
selected = st.selectbox("Person auswählen", options=options, index=selected_index, key="selected_person_box")
if selected != st.session_state.selected_person:
    st.session_state.selected_person = selected
athlet = st.session_state.selected_person

# --- Uploadfelder in einer Zeile am Anfang der Seite ---
col_gpx, col_fit = st.columns(2)
with col_fit:
    st.subheader("FIT-Datei Upload")
    fit_file = st.file_uploader("Lade eine FIT-Datei hoch", type=["fit"], key="fit_uploader")
    st.info("Bitte lade eine FIT-Datei hoch, um sie zu speichern und zu konvertieren.")

with col_gpx:
    st.subheader("GPX-Datenanalyse")
    uploaded_file = st.file_uploader("Lade eine GPX-Datei hoch", type=["gpx"], key="gpx_uploader")
    # Auswahlfeld für vorhandene GPX-Dateien der gewählten Person
    gpx_auswahl = None
    if 'athlet' in locals() and athlet != "Bitte wählen":
        try:
            with open("data/person_db.json", "r", encoding="utf-8") as f:
                db = json.load(f)
            for person in db.get("_default", {}).values():
                name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
                if name == athlet:
                    gpx_files = person.get("gpx_files", [])
                    break
            else:
                gpx_files = []
            if gpx_files:
                gpx_key = "gpx_plot_select"
                if gpx_key not in st.session_state:
                    st.session_state[gpx_key] = gpx_files[0] if gpx_files else None
                gpx_index = gpx_files.index(st.session_state[gpx_key]) if st.session_state[gpx_key] in gpx_files else 0
                selected_gpx = st.selectbox("Wähle eine GPX-Datei zur Visualisierung", gpx_files, index=gpx_index, key="gpx_plot_select_box")
                if selected_gpx != st.session_state[gpx_key]:
                    st.session_state[gpx_key] = selected_gpx
                gpx_auswahl = st.session_state[gpx_key]
            else:
                st.info("Keine GPX-Dateien für diesen Athleten vorhanden.")
        except Exception as e:
            st.error(f"Fehler beim Laden der GPX-Dateien: {e}")
    else:
        gpx_files = []
        gpx_auswahl = None

# --- GPX-Upload: Success/Fehler direkt unter das Uploadfeld (nach Athletenauswahl) ---
with col_gpx:
    if uploaded_file is not None and athlet != "Bitte wählen":
        import os
        gpx_dir = os.path.join("data", "gpx_files")
        os.makedirs(gpx_dir, exist_ok=True)
        gpx_path = os.path.join(gpx_dir, uploaded_file.name)
        with open(gpx_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"GPX-Datei erfolgreich gespeichert: {uploaded_file.name}")
        rel_gpx_path = os.path.relpath(gpx_path).replace('\\', '/')
        try:
            with open("data/person_db.json", "r", encoding="utf-8") as f:
                db = json.load(f)
            for person in db.get("_default", {}).values():
                name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
                if name == athlet:
                    if "gpx_files" not in person:
                        person["gpx_files"] = []
                    if rel_gpx_path not in person["gpx_files"]:
                        person["gpx_files"].append(rel_gpx_path)
                    break
            with open("data/person_db.json", "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            st.success("GPX-Verknüpfung in der Datenbank gespeichert.")
        except Exception as e:
            st.error(f"Fehler beim Speichern der GPX-Verknüpfung in der Datenbank: {e}")
    elif uploaded_file is not None and athlet == "Bitte wählen":
        st.warning("Bitte wähle zuerst einen Athleten aus.")

# --- Layout: linke Spalte GPX, rechte Spalte CSV-Visualisierung ---
main_col_gpx, main_col_csv = st.columns(2)

with main_col_gpx:
    try:
        # Für die Visualisierung: Wenn Auswahl vorhanden, diese Datei verwenden, sonst hochgeladene Datei
        gpx_file_for_plot = None
        if gpx_auswahl:
            gpx_file_for_plot = open(gpx_auswahl, "rb")
        elif uploaded_file is not None:
            gpx_file_for_plot = uploaded_file
        if gpx_file_for_plot:
            gpx_data_pydeck(gpx_file_for_plot)
            gpx_file_for_plot.seek(0)
            fig = gpx_elevation_profile(gpx_file_for_plot)
            st.plotly_chart(fig)
        else:
            st.write("Bitte laden Sie eine GPX-Datei hoch oder wählen Sie eine aus, um die Kartendarstellung zu sehen.")
    except Exception as e:
        st.write(f"Fehler bei der GPX-Visualisierung: {e}")

with main_col_csv:
    # --- CSV-Plot: Spaltenauswahl und Plotly-Diagramm ---
    from src.analyze_data import plot_csv_column_over_time
    if athlet != "Bitte wählen":
        try:
            with open("data/person_db.json", "r", encoding="utf-8") as f:
                db = json.load(f)
            for person in db.get("_default", {}).values():
                name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
                if name == athlet:
                    fit_files = person.get("fit_files", [])
                    break
            else:
                fit_files = []
            if fit_files:
                st.subheader("CSV-Daten visualisieren")
                csv_paths = [pair["csv_path"] for pair in fit_files if "csv_path" in pair]
                csv_key = "csv_plot_select"
                if csv_key not in st.session_state:
                    st.session_state[csv_key] = csv_paths[0] if csv_paths else None
                csv_index = csv_paths.index(st.session_state[csv_key]) if st.session_state[csv_key] in csv_paths else 0
                selected_csv = st.selectbox("Wähle eine CSV-Datei", csv_paths, index=csv_index, key="csv_plot_select_box")
                if selected_csv != st.session_state[csv_key]:
                    st.session_state[csv_key] = selected_csv
                csv_choice = st.session_state[csv_key]
                if csv_choice:
                    import pandas as pd
                    try:
                        df = pd.read_csv(csv_choice)
                    except Exception as e:
                        st.error(f"Fehler beim Laden der Datei {csv_choice}: {e}")
                        import os
                        if not os.path.exists(csv_choice):
                            for pair in fit_files:
                                if pair.get("csv_path") == csv_choice:
                                    fit_files.remove(pair)
                                    break
                            for p in db.get("_default", {}).values():
                                n = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
                                if n == athlet:
                                    p["fit_files"] = fit_files
                                    break
                            with open("data/person_db.json", "w", encoding="utf-8") as f:
                                json.dump(db, f, ensure_ascii=False, indent=2)
                            st.info(f"Eintrag für fehlende Datei {csv_choice} wurde entfernt.")
                            st.rerun()
                        df = None
                    if df is not None:
                        zeit_spalten = [col for col in df.columns if col.lower() in ["timestamp", "time", "zeit"]]
                        if not zeit_spalten:
                            st.warning("Keine Zeitspalte gefunden.")
                        else:
                            time_col = zeit_spalten[0]
                            value_cols = [col for col in df.columns if col != time_col and df[col].notna().any() and (df[col] != '').any()]
                            value_col_key = "csv_value_col"
                            if value_col_key not in st.session_state:
                                st.session_state[value_col_key] = value_cols[0] if value_cols else None
                            value_col_index = value_cols.index(st.session_state[value_col_key]) if st.session_state[value_col_key] in value_cols else 0
                            selected_value_col = st.selectbox("Wähle die zu plottende Spalte", value_cols, index=value_col_index, key="csv_value_col_box")
                            if selected_value_col != st.session_state[value_col_key]:
                                st.session_state[value_col_key] = selected_value_col
                            value_col = st.session_state[value_col_key]
                            if value_col:
                                fig = plot_csv_column_over_time(csv_choice, time_col, value_col)
                                if fig:
                                    st.plotly_chart(fig)
                        if st.button(f"CSV löschen: {csv_choice}", key=f"delete_csv_{csv_choice}"):
                            import os
                            try:
                                os.remove(csv_choice)
                                st.success(f"CSV-Datei {csv_choice} gelöscht.")
                                for pair in fit_files:
                                    if pair.get("csv_path") == csv_choice:
                                        fit_files.remove(pair)
                                        break
                                for p in db.get("_default", {}).values():
                                    n = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
                                    if n == athlet:
                                        p["fit_files"] = fit_files
                                        break
                                with open("data/person_db.json", "w", encoding="utf-8") as f:
                                    json.dump(db, f, ensure_ascii=False, indent=2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Fehler beim Löschen der Datei: {e}")
            else:
                st.info("Keine FIT/CSV-Paare für diesen Athleten vorhanden.")
        except Exception as e:
            st.error(f"Fehler beim Laden der CSV-Plot-Auswahl: {e}")

# --- Neues Feature: FIT-Datei Upload, Speicherung und Konvertierung zu CSV mit Athletenauswahl ---

if fit_file is not None and athlet != "Bitte wählen":
    import os
    fit_dir = os.path.join("data", "fit_files")
    csv_dir = os.path.join("data", "csv_files")
    os.makedirs(fit_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)
    fit_path = os.path.join(fit_dir, fit_file.name)
    with open(fit_path, "wb") as f:
        f.write(fit_file.getbuffer())
    st.success(f"FIT-Datei erfolgreich gespeichert: {fit_file.name}")
    # Konvertiere FIT zu CSV (ohne Athletenname im Dateinamen)
    csv_name = os.path.splitext(fit_file.name)[0] + ".csv"
    csv_path = os.path.join(csv_dir, csv_name)
    try:
        fit_to_csv(fit_path, csv_path)
        st.success(f"CSV-Datei erfolgreich gespeichert: {csv_name}")
        # Verknüpfung in person_db.json speichern
        rel_fit_path = os.path.relpath(fit_path).replace('\\', '/')
        rel_csv_path = os.path.relpath(csv_path).replace('\\', '/')
        try:
            with open("data/person_db.json", "r", encoding="utf-8") as f:
                db = json.load(f)
            # Finde die Person anhand des Namens
            for person in db.get("_default", {}).values():
                name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
                if name == athlet:
                    if "fit_files" not in person:
                        person["fit_files"] = []
                    person["fit_files"].append({"fit_path": rel_fit_path, "csv_path": rel_csv_path})
                    break
            with open("data/person_db.json", "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
            st.success("Verknüpfung in der Datenbank gespeichert.")
        except Exception as e:
            st.error(f"Fehler beim Speichern der Verknüpfung in der Datenbank: {e}")
    except Exception as e:
        st.error(f"Fehler beim Konvertieren der FIT-Datei: {e}")
elif fit_file is not None and athlet == "Bitte wählen":
    st.warning("Bitte wähle zuerst einen Athleten aus.")

# --- GPX-Datei nach Upload mit Athlet in TinyDB JSON verknüpfen ---
if uploaded_file is not None and athlet != "Bitte wählen":
    import os
    gpx_dir = os.path.join("data", "gpx_files")
    os.makedirs(gpx_dir, exist_ok=True)
    gpx_path = os.path.join(gpx_dir, uploaded_file.name)
    with open(gpx_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"GPX-Datei erfolgreich gespeichert: {uploaded_file.name}")
    rel_gpx_path = os.path.relpath(gpx_path).replace('\\', '/')
    try:
        with open("data/person_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
        for person in db.get("_default", {}).values():
            name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
            if name == athlet:
                if "gpx_files" not in person:
                    person["gpx_files"] = []
                if rel_gpx_path not in person["gpx_files"]:
                    person["gpx_files"].append(rel_gpx_path)
                break
        with open("data/person_db.json", "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        st.success("GPX-Verknüpfung in der Datenbank gespeichert.")
    except Exception as e:
        st.error(f"Fehler beim Speichern der GPX-Verknüpfung in der Datenbank: {e}")

# --- FIT/CSV-Paare für den ausgewählten Athleten anzeigen und löschen ---
if athlet != "Bitte wählen":
    try:
        with open("data/person_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
        # Finde die Person anhand des Namens
        for person in db.get("_default", {}).values():
            name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
            if name == athlet:
                fit_files = person.get("fit_files", [])
                break
        else:
            fit_files = []
        if fit_files:
            st.subheader("FIT/CSV-Paare löschen")
            for i, file_pair in enumerate(fit_files):
                col1, col2, col3 = st.columns([4, 4, 1])
                with col1:
                    st.write(f"FIT: {file_pair.get('fit_path','')}")
                with col2:
                    st.write(f"CSV: {file_pair.get('csv_path','')}")
                with col3:
                    if st.button("Löschen", key=f"delete_fit_{i}"):
                        import os
                        # Lösche Dateien
                        for path in [file_pair.get("fit_path"), file_pair.get("csv_path")]:
                            if path and os.path.exists(path):
                                try:
                                    os.remove(path)
                                except Exception as e:
                                    st.warning(f"Konnte Datei {path} nicht löschen: {e}")
                        # Entferne Eintrag aus der Datenbank
                        fit_files.pop(i)
                        # Schreibe zurück
                        for p in db.get("_default", {}).values():
                            n = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
                            if n == athlet:
                                p["fit_files"] = fit_files
                                break
                        with open("data/person_db.json", "w", encoding="utf-8") as f:
                            json.dump(db, f, ensure_ascii=False, indent=2)
                        st.success("FIT/CSV-Paar gelöscht.")
                        st.rerun()
        else:
            st.info("Keine FIT/CSV-Paare für diesen Athleten vorhanden.")
    except Exception as e:
        st.error(f"Fehler beim Laden der FIT/CSV-Paare: {e}")

# --- GPX-Dateien für den ausgewählten Athleten anzeigen und löschen ---
if athlet != "Bitte wählen":
    try:
        with open("data/person_db.json", "r", encoding="utf-8") as f:
            db = json.load(f)
        # Finde die Person anhand des Namens
        for person in db.get("_default", {}).values():
            name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
            if name == athlet:
                gpx_files = person.get("gpx_files", [])
                break
        else:
            gpx_files = []
        if gpx_files:
            st.subheader("GPX-Dateien löschen")
            for i, gpx_path in enumerate(gpx_files):
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.write(f"GPX: {gpx_path}")
                with col2:
                    if st.button("Löschen", key=f"delete_gpx_{i}"):
                        import os
                        if gpx_path and os.path.exists(gpx_path):
                            try:
                                os.remove(gpx_path)
                            except Exception as e:
                                st.warning(f"Konnte GPX-Datei {gpx_path} nicht löschen: {e}")
                        # Entferne Eintrag aus der Datenbank
                        gpx_files.pop(i)
                        # Schreibe zurück
                        for p in db.get("_default", {}).values():
                            n = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip()
                            if n == athlet:
                                p["gpx_files"] = gpx_files
                                break
                        with open("data/person_db.json", "w", encoding="utf-8") as f:
                            json.dump(db, f, ensure_ascii=False, indent=2)
                        st.success("GPX-Datei gelöscht.")
                        st.rerun()
        else:
            st.info("Keine GPX-Dateien für diesen Athleten vorhanden.")
    except Exception as e:
        st.error(f"Fehler beim Laden der GPX-Dateien: {e}")
