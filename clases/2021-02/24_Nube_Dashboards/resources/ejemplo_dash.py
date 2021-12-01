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
