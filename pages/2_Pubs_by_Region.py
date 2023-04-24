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
region = st.selectbox("Select Region", ('Region', *regions))

for reg in regions:
    if region == reg:
        areas = df[df['region'] == reg]['area'].unique().tolist()
        area = st.selectbox("Select Area", areas)
        for ar in areas:
            if area == ar:
                area_df = df[(df['region'] == reg) & (df['area'] == ar)]
                m = folium.Map(location=[area_df['latitude'].mean(), area_df['longitude'].mean()],
                               control_scale=True)
                for i, row in area_df.iterrows():
                    html = f"""
                            <h4>Name: {row["name"]}</h4>
                            <p>{row["address"]}</p>
                            """
                    iframe = folium.IFrame(html=html, width=200, height=150)
                    popup = folium.Popup(iframe)
                    folium.Marker(location=[row['latitude'], row['longitude']],
                                  icon=folium.Icon(color='orange', icon='beer-mug-empty', prefix='fa'),
                                  popup=popup).add_to(m)
                sw = area_df[['latitude', 'longitude']].min().values.tolist()
                ne = area_df[['latitude', 'longitude']].max().values.tolist()
                m.fit_bounds([sw, ne])
                folium_static(m, width=700)
