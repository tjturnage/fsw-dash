import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)
feedback = {'border': '2px gray solid', 'padding':'1em'}
layout = dbc.Container([

        #############
        # View output
        #############
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Download FSW Output", id="download-btn", color="success", style={'padding':'1em','width':'100%'}),
                    dcc.Download(id="download")
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Show File Content", id="display-file-content-btn", color="success", style={'padding':'1em','width':'100%'}),
                ])
            )
        ]),        
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Div(children="File output will display here... ",id="display-file-content-response",style=feedback)
                ])
            )
        ]),  
    ]),