import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import utils

new_df = pd.read_csv("pages/data/new_df.csv")
new_df.columns = (x.replace(" ", "_").replace("<1","") for x in new_df.columns)
new_df = new_df[["valor_real", "valor_previsto", "porcentagem", 
                 "categoria_desconto", "H_OCEAN", "NEAR_OCEAN", 
                 "NEAR_BAY", "ISLAND", "INLAND", "latitude", "longitude"]]

value = st.sidebar.slider("Valor do imóvel", 0, 500003, 500003, step=5)
proximity = st.sidebar.multiselect("Próxima da praia?", 
                                   options=["<1h do oceano",
                                            "Próximo do oceano",
                                            "Próximo da praia",
                                            "Ilha",
                                            "Interior"])

prox_dict = {"<1h do oceano": "H_OCEAN",
             "Próximo do oceano": "NEAR_OCEAN",
             "Próximo da praia": "NEAR_BAY",
             "Ilha": "ISLAND",
             "Interior": "INLAND"}

proximity = (prox_dict[prox] for prox in proximity)

new_df = new_df.loc[new_df["valor_real"] < value]

query = str()
for i, feature in enumerate(proximity):
    query += f" | {feature} == 1" if i > 0 else f"{feature} == 1"

if len(query) > 0:
        new_df = new_df.query(query)
else:
      pass

st.dataframe(new_df)

figd = px.scatter(new_df, x="longitude", y="latitude", color="categoria_desconto", 
        width=800, height=400)

st.plotly_chart(figd)