import pydeck as pdk
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb
import matplotlib.pyplot as plt

def plot_estatico(data, criterio):
    fig, ax = plt.subplots(1, figsize=(5, 8))

    label_mask = ["Valor médio das casas", "Idade média das casas"]
    dict_label = dict(zip(["value", "age"], label_mask))
    label = dict_label[criterio] if criterio in ["value", "age"] else "X"

    data.plot(column=criterio,
            legend=True,
            legend_kwds={
                "label": label,
                "orientation": "vertical",
                "shrink": 0.4,
                },
            ax = ax);
    ax.axis("off");

    return fig

def distritos(data, extrude, column):
    # Escolher uma palheta de cores e quantidade de cores diferentes a serem usadas
    palette = "Blues"
    n_colors = 5
    colors = cm.get_palette(palette, n_colors)
    colors = [hex_to_rgb(c) for c in colors] # Passar as cores para hex


    # Para cada estado, pintar ele baseado no valor das casas (normalizado)
    for i, ind in enumerate(data.index):
        proportion = ((data.loc[ind, column] - data[column].min())/ (data[column].max() - data[column].min()))
        index = int(round(n_colors * proportion, 0))

        if index >= len(colors):
            index = len(colors) - 1
        data.loc[ind, "R"] = colors[index][0]
        data.loc[ind, "G"] = colors[index][1]
        data.loc[ind, "B"] = colors[index][2]


    geojson = pdk.Layer(
            "GeoJsonLayer",
            data,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            extruded=extrude,
            wireframe=True,
            get_elevation=column,
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

    return r

def plot_3d(data):
    layer = pdk.Layer('HexagonLayer',
        data,
        get_position=['longitude', 'latitude'],
        auto_highlight=True,
        pickable=True,
        get_elevation="value",
        extruded=True,
        elevation_scale=100,
        coverage=1)

    # Set the viewport location
    view_state = pdk.ViewState(
        latitude=36.3, 
        longitude=-119.6194155,
        zoom=5,
        min_zoom=5,
        max_zoom=15,
        pitch=50.5,
        bearing=27.36)

    # Combined all of it and render a viewport
    r2 = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="dark")

    return r2