import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
DATA_PATH = os.path.join(PARENT_DIR, "data", "pubs.csv")

@st.cache_data
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


df = load_dataset(DATA_PATH)
regions = ['Greater London',
           'East of England',
           'East Midlands',
           'North East',
           'South East',
           'West Midlands',
           'North West',
           'South West',
           'Scotland',
           'Wales']

st.markdown("### Map of Pubs by Region in the UK")
region = st.selectbox("Select Region", (None, *regions))

for reg in regions:
    if region == reg:
        reg_df = df[df['Region'] == reg]
        m = folium.Map(location=[reg_df['latitude'].mean(), reg_df['longitude'].mean()],
                       zoom_start=14, control_scale=True)
        for i, row in reg_df.iterrows():
            html = f"""
                    <h4>Name: {row["name"]}</h4>
                    <p>{row["address"]}</p>
                    """
            iframe = folium.IFrame(html=html, width=200, height=150)
            popup = folium.Popup(iframe)
            folium.Marker(location=[row['latitude'], row['longitude']],
                          icon=folium.Icon(color='orange', icon='beer-mug-empty', prefix='fa'),
                          popup=popup).add_to(m)
        sw = reg_df[['latitude', 'longitude']].min().values.tolist()
        ne = reg_df[['latitude', 'longitude']].max().values.tolist()
        m.fit_bounds([sw, ne])
        folium_static(m, width=700)
