import gpxpy
import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st
import json
from geopy.distance import geodesic
import plotly.graph_objects as go

def gpx_data(uploaded_file):
    if uploaded_file is not None:
        gpx_content = uploaded_file.read().decode("utf-8")  # Lies und dekodiere den Inhalt
        gpx = gpxpy.parse(gpx_content)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append({
                        "lat": point.latitude,
                        "lon": point.longitude,
                        "elevation": point.elevation
                    })
        if points:
            df = pd.DataFrame(points)
            fig = px.line_mapbox(
                df,
                lat="lat",
                lon="lon",
                hover_data=["elevation"],
                zoom=10,
                height=500
            )
    return fig

def gpx_data_pydeck(uploaded_file):
    """ 
    Eine Funktion, welche die ausgewählte GPX-Datei verarbeitet 
    und auf einer für Outdooraktivitäten optimierten Karte anzeigt, die in einer 3D-Version verfügbar ist.
    """
    if uploaded_file is not None:
        gpx_content = uploaded_file.read().decode("utf-8")  # Lies und dekodiere den Inhalt
        gpx = gpxpy.parse(gpx_content)
        path = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    path.append([point.longitude, point.latitude, point.elevation])

    if path:
        df = pd.DataFrame([{"path": path}])
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/outdoors-v11",
            initial_view_state=pdk.ViewState(
                latitude=path[0][1],
                longitude=path[0][0],
                zoom=9.9,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "PathLayer",
                    data=df,
                    get_path="path",
                    get_color=[255, 0, 0],
                    width_scale=10,
                    width_min_pixels=2,
                    get_width=0.2,
                    elevation_scale=0,
                    pickable=True,
                ),
            ],
        ))
    else:
        st.warning("Keine GPS-Punkte in der GPX-Datei gefunden.")
    return st.pydeck_chart

def gpx_elevation_profile(uploaded_file):
    """ 
    Eine Funktion, die das Höhenprofil aus einer GPX-Datei extrahiert und als Plotly-Diagramm darstellt.
    """
    if uploaded_file is not None:
        gpx_content = uploaded_file.read().decode("utf-8")  # Lies und dekodiere den Inhalt
        gpx = gpxpy.parse(gpx_content)

    elevation = []
    distance = [0]
    last_point = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                elevation.append(point.elevation)
                if last_point:
                    dist = geodesic(
                        (last_point.latitude, last_point.longitude),
                        (point.latitude, point.longitude)
                    ).meters
                    distance.append(distance[-1] + dist)
                last_point = point

    fig = go.Figure(data=go.Scatter(x=distance, y=elevation, mode='lines', name='Höhenprofil'))
    fig.update_layout(
        title='Höhenprofil',
        xaxis_title='Distanz (m)',
        yaxis_title='Höhe (m)',
    )
    return fig