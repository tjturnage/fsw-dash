from datetime import datetime
from gc import callbacks
import numpy as np


import re
from textwrap import wrap
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
#import plotly.graph_objs as go
import pandas as pd
import glob
import os

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.DARKLY])#, 'https://codepen.io/chriddyp/pen/bWLwgP.css'])

now = datetime.utcnow()
endyear = now.year + 1
try:
    os.list('/data/')
    root_dir = '/data'
    FSW_DIR = '/Forecast_Search_Wizard'
    DATA_DIR = os.path.join(root_dir, 'TEXT_DATA')
    FSW_OUTPUT_DIR = os.path.join(FSW_DIR,'FSW_OUTPUT')

except:
    root_dir = 'C:/data/'
    #root_dir = '/home/tjturnage/'

card_content = [
            dbc.CardBody([html.H1("Forecast Search Wizard", className="card-title"),
                html.H3(
                    "An application to search National Weather Service Text Products by keywords",
                    className="card-text",
                ),
                dbc.CardLink("Details at GitHub repository", href="https://github.com/allenea/Forecast_Search_Wizard"),
            ])
]


app.layout = dbc.Container(
    html.Div([
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        dbc.Row(dbc.Card(card_content, color="primary", inverse=True)),
        dbc.Row(
            html.Div([
                html.H3(children="Step 1: Enter Products in upper case, separated by spaces"),
                html.Div([dbc.Input(id='list-in',placeholder='AFDGRR AFDAPX',type='text')],
                style=dict(display='flex', width='100%', size='600')),
                html.Div([dbc.Button("Create Product List",id='submit-button', n_clicks=0)]),
                html.Div(id='list-out', style={'border': '2px gray solid'},)])
        ),
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        html.Div([html.H3(children="Step 2: Choose Range of Years to Search"),]),
        dbc.Row([

            dbc.Col(
                dcc.RangeSlider(
                id="slider",
                min=1996,
                max=2022,
                value=[2010, 2020],
                marks={i: str(i) for i in range(1996,2023)},
                )
            )
    ],
    style={"padding": "50px"},
    )

    ])
)


@app.callback(Output(component_id='list-out', component_property='children'),
                [Input(component_id='submit-button',component_property='n_clicks')],
                [State('list-in','value')])

def create_list(n_clicks,myvalue):
    input_string = str(myvalue)
    product_list = input_string.split(' ')
    return str(product_list)

if __name__ == '__main__':
    app.run_server()