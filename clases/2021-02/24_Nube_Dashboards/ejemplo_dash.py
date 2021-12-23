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
    df, x="body_mass_g", color="species", barmode="group", title="Histograma"
)

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
            ],
            style={"display": "flex", "justify-content": "space-between"},
        ),
    ]
)


@app.callback(
    Output("histograma-principal", "figure"), Input("select", "value"),
)
def update_histograma(col_select,):
    print("Parámetros:", col_select)

    fig = px.histogram(
        df, x=col_select, color="species", barmode="overlay", title="Histograma",
    )
    return fig


# --------------------------------------------------------------------------------------
# Ejecutamos el servidor. (usar python ejemplo_dash.py)
if __name__ == "__main__":
    app.run_server(debug=True)

