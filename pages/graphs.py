import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, order=3, location = "sidebar")
feedback = {'border': '2px gray solid', 'padding':'1em'}

layout = dbc.Container([
    dcc.Markdown("This will be the graph page")])