import streamlit as st
#import plotly.express as px
import pandas as pd
import geopandas as gpd
import utils

cali = gpd.read_file('data/cali.shp') 
df = pd.read_csv("data/df.csv")

st.title("Análise de Critérios por Região\n")
#st.write("Vamos ver como o preço de casas na Califórnia varia por região.")

opcoes = ["Idade média das casas", "Receita média das famílias",
            "Valor médio das casas", "Proximidade do oceano",
            "Categoria de valor", "Número de quartos por pessoa",
            "Número de salas por pessoa", "Número de quartos por sala",
            "Número de pessoas por família"]
masks = list(df.columns)[3:]
dict_opcoes = dict(zip(opcoes, masks))

# Plot estático
geo_cat = st.sidebar.selectbox('Critério', 
                                options = opcoes)
radio_b = st.sidebar.checkbox("Visualização 3D")

criterio_escolhido = dict_opcoes[geo_cat]

st.pyplot(utils.plot_estatico(cali, criterio_escolhido))
#st.pydeck_chart(utils.distritos(cali, radio_b, criterio_escolhido))