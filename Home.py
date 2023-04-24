import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(FILE_DIR, "image", "pub.jpg")
DATA_PATH = os.path.join(FILE_DIR, "data", "pubs.csv")


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
colors = ['blue', 'white', 'red', 'blue', 'red', 'blue', 'red', 'white', 'blue']

st.markdown('## Welcome to pub-finding App')
img = plt.imread(IMAGE_PATH)
st.image(img, width=500)
st.markdown('In this App:')

for color, region in zip(colors, regions):
    pubs_num = len(df[df['region'] == region])
    st.write(f':{color}[There are _{pubs_num}_ pubs available for you in **{region}**.]')
st.write('')
st.write('')
st.caption(':blue[My] [Linkedin](https://www.linkedin.com/in/natalia-khripkova/) :blue[account]')
st.caption(':blue[App] [GitHub](https://github.com/KhripkovaNA/Pub_finding_App) :blue[repo]')
st.caption('Innomatics Research Labs Internship - February 2023')
