import streamlit as st
#import plotly.express as px
import pandas as pd
import geopandas as gpd
import utils

cali = gpd.read_file('data/cali.shp') 
df = pd.read_csv("data/df.csv")

st.markdown("""<h1 style='text-align: center;'>Visualização do valor  das casas</h1>""", unsafe_allow_html=True)
st.markdown("""No gráfico abaixo, a altura dos polígonos indica o preço médio dos imóveis na região.
            Você pode dar zoom com o scroll do mouse, arrastar com o botão esquerdo para mover o mapa e \
                segurar CTRL enquanto segura o botão esquerdo do mouse para rotacionar o mapa""")

st.sidebar.markdown('## Defina o Preço da Casa')
valor_min, valor_max = st.sidebar.slider("Escolha o intervalo de valores", 0, 500003, (0, 500003), step=5)

# Mostrar o valor selecionado na sidebar
st.sidebar.markdown(f"Valor mínimo: $ {valor_min:,.0f}")
st.sidebar.markdown(f"Valor máximo: $ {valor_max:,.0f}")

# Criar o plot 3D
st.pydeck_chart(utils.plot_3d(df))

st.markdown("""Os valores mais específicos dos imóveis em cada região podem ser visualizados na página \
    de análise por distrito""")