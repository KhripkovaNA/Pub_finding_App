import streamlit as st
import pandas as pd
import os


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
DATA_PATH = os.path.join(PARENT_DIR, "data", "pubs.csv")

@st.cache_data
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


df = load_dataset(DATA_PATH)

st.markdown("### Pubs in the UK")
st.map(df, zoom=4)
