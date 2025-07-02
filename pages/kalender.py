import streamlit as st
from datetime import date
from streamlit_calendar import calendar
import json
# hello
st.set_page_config(
    page_title="Kalender",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("📅 Kalender")
    st.subheader("Willkommen im Kalender-Bereich!")
    st.write("Hier werden Ihnen alle EKG-Tests der Athleten angezeigt.")

# Interaktive Monatsansicht mit streamlit-calendar
st.subheader("Monatsansicht")

calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "de",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "buttonText": {
        "today": "Heute",
        "month": "Monat",
        "week": "Woche",
        "day": "Tag",
        "list": "Liste",
        "prev": "Zurück",
        "next": "Vor"
    }
}

# Events für alle verfügbaren Tests aus person_db.json generieren
with open("data/person_db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

events = []
for person in db.get("_default", {}).values():
    name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
    for test in person.get("ekg_tests", []):
        # Datum ins ISO-Format (YYYY-MM-DD) umwandeln
        try:
            day, month, year = test["date"].split(".")
            iso_date = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
        except Exception:
            iso_date = test["date"]
        events.append({
            "title": f"EKG-Test: {name}",
            "start": iso_date,
            "allDay": True,
            "url": test.get("result_link", "")
        })

calendar(
    events=events,
    options=calendar_options,
    custom_css="",
    key="calendar_month_view"
)
