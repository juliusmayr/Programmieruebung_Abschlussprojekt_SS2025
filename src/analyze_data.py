import gpxpy
import pandas as pd
import plotly.express as px

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