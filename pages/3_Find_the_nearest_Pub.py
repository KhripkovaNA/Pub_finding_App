import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
from geopy import distance

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
DATA_PATH = os.path.join(PARENT_DIR, "data", "pubs.csv")


@st.cache_data
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


df = load_dataset(DATA_PATH)

st.markdown("### Find 5 nearest Pubs")
col1, col2, col3 = st.columns(3)
with col1:
    lat = st.number_input("Latitude:",
                          value=51.50563667901435,
                          step=0.0000000000001,
                          format="%0.13f",
                          help="in decimal degrees")
with col2:
    lon = st.number_input("Longitude:",
                          value=-0.07533504629225196,
                          step=0.0000000000001,
                          format="%0.13f",
                          help="in decimal degrees")
with col3:
    st.write('')
    st.write('')
    submit = st.button("Find Pubs")

if submit:
    df['distance'] = df.apply(lambda x: distance.distance((lat, lon), (x['latitude'],
                                                                       x['longitude'])).meters,
                              axis=1)
    nearest_pubs = df.sort_values('distance').head()
    m = folium.Map(location=[nearest_pubs['latitude'].mean(), nearest_pubs['longitude'].mean()],
                   control_scale=True)
    for i, row in nearest_pubs.iterrows():
        html = f"""
                <h4>Name: {row["name"]}</h4>
                <p>Address: {row["address"]}</p>
                """
        iframe = folium.IFrame(html=html, width=200, height=150)
        popup = folium.Popup(iframe)
        folium.Marker(location=[row['latitude'], row['longitude']],
                      icon=folium.Icon(color='orange', icon='beer-mug-empty', prefix='fa'),
                      popup=popup).add_to(m)
    popup = folium.Popup(folium.IFrame(html=f"<h4>You are here</h4>", width=150, height=50))
    folium.Marker(location=[lat, lon],
                  icon=folium.Icon(color='red', icon='user', prefix='fa'),
                  popup=popup).add_to(m)
    coords = nearest_pubs[['latitude', 'longitude']]
    coords = pd.concat([coords, pd.DataFrame({'latitude': [lat], 'longitude': [lon]})],
                       axis=0, ignore_index=True)
    sw = coords[['latitude', 'longitude']].min().values.tolist()
    ne = coords[['latitude', 'longitude']].max().values.tolist()
    m.fit_bounds([sw, ne])
    folium_static(m, width=700)
