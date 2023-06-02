import streamlit as st
#import plotly.express as px
import pandas as pd
import geopandas as gpd
import utils
from st_pages import Page, show_pages
from PIL import Image

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/2_Database.py", "Database", "🥼"),
        Page("pages/3_District_analysis.py", "District analysis", "🌐"),
        Page("pages/4_Find_your_home.py", "Find your home", "🙌")
    ]
)

description = """ Esse projeto é um exercício de ciência de dados que tem como objetivo utilizar \
        um dos bancos de dados mais conhecidos do mundo, o California Housing Prices, para desenvolver \
        uma análise o mais aprofundada possível das características do setor imobiliário da Califórnia, \
        desenvoler um dashboard ou site para apresentação de resultados e aplicar técnicas de machine learning \
        para desenvolvimento de uma ferramenta que poderia ser usada para resolver problemas reais."""

st.markdown("""<h1 style='text-align: center;'>Califórnia Housing Prices</h1>""", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Sejam bem-vindos ao dashboard do projeto Califórnia da Liga de Data Science!!</h2>", unsafe_allow_html=True)
st.markdown(description)

col1, col2, col3, col4 = st.columns(4, gap="small")

with col2:
    image = Image.open('images\LogoDS.png')
    st.image(image, width=360)

st.text("Membros devs 💓👉 Ana, Harry, Dos100, Mari, Murilo, Victor e Arara")
