import gpxpy
import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st


def gpx_data(uploaded_file):
    
    if uploaded_file is not None:
        gpx = gpxpy.parse(uploaded_file)
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

    if uploaded_file is not None:
        gpx = gpxpy.parse(uploaded_file)
        path = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    path.append([point.longitude, point.latitude])

    if path:
        df = pd.DataFrame([{"path": path}])
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/outdoors-v11",
            initial_view_state=pdk.ViewState(
                latitude=path[0][1],
                longitude=path[0][0],
                zoom=10,
                pitch=60,
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