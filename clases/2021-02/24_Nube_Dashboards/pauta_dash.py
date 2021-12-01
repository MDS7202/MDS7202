# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, dcc, html

# --------------------------------------------------------------------------------------
# Iniciamos el server
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# --------------------------------------------------------------------------------------
# Cargamos el dataset y generamos un gráfico de plotly.
df = pd.read_csv("./resources/penguins.csv")
fig = px.histogram(
    df, x="body_mass_g", color="species", barmode="overlay", title="Histograma"
)
geo_df = gpd.read_file("./resources/comunas.geojson")


censo = pd.read_excel("./resources/censo.xlsx", sheet_name="COMUNAS", header=0)

total_comunal = censo[censo["Edad"] == "Total Comunal"]

geo_df = geo_df.merge(total_comunal, left_on="comuna_id", right_on="Código Comuna")
# generar figura
fig_mapa = px.choropleth(
    geo_df,
    geojson=geo_df.geometry,
    locations=geo_df.index,
    color="TOTAL",
    projection="mercator",
    fitbounds=False,
    basemap_visible=False,
    scope="south america",
    title="Población en Chile por Comuna",
    height=800,
)


# --------------------------------------------------------------------------------------
# Definimos el layout -> Los elementos de la página

app.layout = html.Div(
    children=[
        # titulo
        html.H1("Mi primer Dashboard usando Dash 📈"),
        # contenedor (pensemos que es una fila)
        html.Div(
            [
                html.Img(
                    src="https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/man/figures/lter_penguins.png",
                    alt="Pinguinos de Palmer!",
                    style={  # estilos de la imagen.
                        "max-width": "600px",  # que no ocupe más del 100% del espacio de su padre (div)
                        "height": "auto",  # que la altura se autocalcule
                        "object-fit": "contain",  # que no se estire la imagen.
                    },
                ),
            ],
            style={"display": "flex", "justify-content": "center"},
        ),
        html.Div([dcc.Graph(id="histograma-principal", figure=fig)],),
        html.Div(
            [html.H5("Opciones de la visualización")], style={"margin-bottom": 20}
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="select",
                    options=[{"label": k, "value": k} for k in df.columns],
                    value="body_mass_g",
                    style={"margin": 12, "flex": 1},
                ),
                html.Div(
                    [
                        html.P("Histnorm"),
                        dcc.RadioItems(
                            id="histnorm",
                            options=[
                                {"label": "Porcentaje", "value": "percent"},
                                {"label": "Probabilidad", "value": "probability"},
                            ],
                            value="percent",  # valor por defecto
                        ),
                    ],
                    style={"margin": 12, "flex": 1},
                ),
                html.Div(
                    [
                        html.P("Número de Bins"),
                        dcc.Input(
                            id="nbins",
                            type="number",
                            value=10,  # valor por defecto
                            min=10,
                            max=50,
                            step=5,
                        ),
                    ],
                    style={"margin": 12, "flex": 1},
                ),
            ],
            style={"display": "flex", "justify-content": "space-between"},
        ),
        html.Div([html.H5("Tabla de Datos")], style={"margin-bottom": 20}),
        # https://dash.plotly.com/datatable
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in censo.columns],
            data=censo.to_dict("records"),
            export_format="xlsx",
            sort_action="native",
            filter_action="native",
            page_size=25,
        ),
        html.Div([dcc.Graph(id="mapa-poblacion", figure=fig_mapa)],),
    ],
    style={"margin": "24px"},
)


@app.callback(
    Output("histograma-principal", "figure"),
    Input("select", "value"),
    Input("histnorm", "value"),
    Input("nbins", "value"),
)
def update_histograma(col_select, histnorm, nbins):
    print("Parámetros:", col_select, histnorm, nbins)

    fig = px.histogram(
        df,
        x=col_select,
        color="species",
        barmode="overlay",
        title="Histograma",
        histnorm=histnorm,
        nbins=nbins,
    )
    return fig


# --------------------------------------------------------------------------------------
# Ejecutamos el servidor. (usar python ejemplo_dash.py)
if __name__ == "__main__":
    app.run_server(debug=True)

