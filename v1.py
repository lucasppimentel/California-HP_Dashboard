import streamlit as st
#import plotly.express as px
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb


# Puxar os dados prontos
# ****Baixar o cali com todos os atributos*****
cali = gpd.read_file('data/cali.shp') 
df = pd.read_csv("data/df.csv")



# =========================== Estrutura do dashboard ============================
st.title("Análise do Preço por Região\n")
st.write("Vamos ver como o preço de casas na Califórnia varia por região.")

# Filtros para a tabela
checkbox_mostrar_tabela = st.sidebar.checkbox('Mostrar tabela', value = True)

if checkbox_mostrar_tabela:
    
    # Caixa de seleção dos gráficos
    st.sidebar.markdown('## Filtro para a tabela')
    categorias = ["geop", "g2", "g3", "g4"]
    categoria = st.sidebar.selectbox('Selecione a região para visualizar o gráfico',
                                     options = categorias)

    if categoria == 'g4':
        st.sidebar.markdown('## Defina o Preço da Casa')
        valor_min, valor_max = st.sidebar.slider("Escolha o intervalo de valores", 0, 500003, (0, 500003), step=5)

        # Mostrar o valor selecionado na sidebar
        st.sidebar.markdown(f"Valor mínimo: $ {valor_min:,.0f}")
        st.sidebar.markdown(f"Valor máximo: $ {valor_max:,.0f}")
    elif categoria == "geop":
        geo_cats = list(df.columns)[3:]
        geo_cat = st.sidebar.selectbox('Categoria do gráfico', 
                                       options = geo_cats)
        radio_b = st.sidebar.checkbox("Visualização 3D")
    else:
        pass
# ===========================================================================







# ========================= Montar gráfico de distrito ===========================
# Escolher uma palheta de cores e quantidade de cores diferentes a serem usadas
palette = "Blues"
n_colors = 5
colors = cm.get_palette(palette, n_colors)
colors = [hex_to_rgb(c) for c in colors] # Passar as cores para hex


# Para cada estado, pintar ele baseado no valor das casas (normalizado)
for i, ind in enumerate(cali.index):
  proportion = ((cali.loc[ind, geo_cat] - cali[geo_cat].min())/ (cali[geo_cat].max() - cali[geo_cat].min()))
  index = int(round(n_colors * proportion, 0))

  if index >= len(colors):
      index = len(colors) - 1
  cali.loc[ind, "R"] = colors[index][0]
  cali.loc[ind, "G"] = colors[index][1]
  cali.loc[ind, "B"] = colors[index][2]


geojson = pdk.Layer(
        "GeoJsonLayer",
        cali,
        pickable=True,
        opacity=0.5,
        stroked=True,
        filled=True,
        extruded=radio_b,
        wireframe=True,
        get_elevation=geo_cat,
        elevation_scale=1,
        # get_fill_color="color",
        get_fill_color=f"[R, G, B]",
        get_line_color=[0, 0, 0],
        get_line_width=2,
        line_width_min_pixels=1,
    )


# Posição inicial do mapa
view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=4.5, bearing=0, pitch=0)

# Gerar mapa
layers = [geojson]
r = pdk.Deck(
    layers=layers,
    map_style="light",
    initial_view_state=view_state
)


st.pydeck_chart(r)
# ===========================================================================










# ========================== Montar gráfico dos bairros ======================
# df = df[(df['median_house_value'] >= valor_min) & (df['median_house_value'] <= valor_max)]

# # px.scatter_mapbox é um comando que permite visualizar um gráfico de distribuição em forma de caixa
# # 1º especifiquei o dataset df
# # 2º após relacionei lat e lon com a primeira e segunda coluna do df
# # 3º color='Proximidade do mar', permite com que de acordo com a localidade que para o nosso caso são 5, faça uma cor pra cada local
# # 4º mapbox_style, permite a utilização do mapa aberto

# df['median_house_value'] = df['median_house_value'].apply(lambda x: "${:,.0f}".format(x))

# colors = ['purple', 'gray', 'pink', 'red', 'green'] # lista de cores
# latitude_central, longitude_central = (df["latitude"].mean(), df["longitude"].mean())

# fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color = "ocean_proximity", text = df['median_house_value']
#                         ,mapbox_style="open-street-map", zoom=5, color_discrete_sequence = colors,
#                         height=800, center = dict(lat=latitude_central, lon=longitude_central))




# Adicione o gráfico ao Streamlit
#st.plotly_chart(fig)
# =============================================================================



# =============================== Display dos gráficos ========================

# =============================================================================