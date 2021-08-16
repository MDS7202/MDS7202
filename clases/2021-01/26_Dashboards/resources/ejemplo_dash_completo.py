# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


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


# --------------------------------------------------------------------------------------
# Definimos el layout -> Los elementos de la página

app.layout = html.Div(
    children=[
        # titulo
        html.H1(children="Mi primer Dashboard de Dash con Pinguinos"),
        # contenedor (pensemos que es una fila)
        html.Div(
            [
                # primera columna de la fila (la imagen de los pinguinos)
                html.Div(
                    [
                        html.Img(
                            src="https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/man/figures/lter_penguins.png",
                            alt="Pinguinos de Palmer!",
                            style={  # estilos de la imagen.
                                "max-width": "100%",  # que no ocupe más del 100% del espacio de su padre (div)
                                "height": "auto",  # que la altura se autocalcule
                                "object-fit": "contain",  # que no se estire la imagen.
                            },
                        ),
                    ],
                    style={
                        "display": "flex",  # flexbox, permite asignar espacios de forma dinámica.
                        "justify-content": "center",
                    },
                ),
                # segunda columna de la fila, que contiene el histograma
                html.Div(
                    [dcc.Graph(id="histograma-principal", figure=fig)],
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex"},
        ),
        # fila con las opciones de visualizacion
        html.Div(
            [
                # columna 1
                html.Div(
                    [
                        dcc.Dropdown(
                            id="select",
                            options=[{"label": k, "value": k} for k in df.columns],
                            value="body_mass_g",
                        )
                    ],
                    style={"width": "50%"},
                ),
                # columna 2: tipo de
                html.Div(
                    [
                        dcc.RadioItems(
                            id="radio",
                            options=[
                                {"label": k.title(), "value": k}
                                for k in [
                                    "percent",
                                    "probability",
                                    "probability density",
                                ]
                            ],
                            value="percent",  # valor por defecto
                        )
                    ],
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex"},
        ),
    ],
)


@app.callback(
    Output("histograma-principal", "figure"),
    Input("select", "value"),
    Input("radio", "value"),
)
def update_histograma(col_select, histnorm):
    print(histnorm)
    # generamos la figura a partir de los
    fig = px.histogram(
        df,
        x=col_select,
        color="species",
        barmode="overlay",
        title="Histograma",
        histnorm=histnorm,
    )
    return fig


# --------------------------------------------------------------------------------------
# Ejecutamos el servidor. (usar python ejemplo_dash.py)
if __name__ == "__main__":
    app.run_server(debug=True)

