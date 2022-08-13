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
app.title = "Forecast Search Wizard"

now = datetime.utcnow()
endyear = now.year + 1
try:
    os.list('/data/')
    root_dir = '/data'
    cloud = True
    FSW_DIR = '/Forecast_Search_Wizard'
    DATA_DIR = os.path.join(root_dir, 'TEXT_DATA')
    FSW_OUTPUT_DIR = os.path.join(FSW_DIR,'FSW_OUTPUT')

except:
    root_dir = 'C:/data/'
    cloud = False
    #root_dir = '/home/tjturnage/'

def get_text_output():
    if cloud:
        fname = os.listdir(FSW_OUTPUT_DIR)[-1]
        text_file_path = os.join(FSW_OUTPUT_DIR,fname)
        fin = open(text_file_path, 'r')
        text_data = fin.read()
        fin.close()
        return text_data
    else:
        return "Not in instance!"



card_content = [
            dbc.CardBody([html.H1("Forecast Search Wizard", className="card-title"),
                html.H3(
                    "An application to search National Weather Service Text Products by keywords",
                    className="card-text",
                ),
                html.H4(
                    "Developed by Eric Allen (eric.allen@noaa.gov)",
                    className="card-text",
                ),
                dbc.CardLink("Details at GitHub repository", href="https://github.com/allenea/Forecast_Search_Wizard"),
            ])
]

step_one = [
            dbc.CardBody([html.H4("Step 1", className="card-title"),
                html.H5(
                    "Enter Products in upper case and separated by spaces. Click to create product list.",
                    className="card-text",
                ),
            ])
]

step_two = [
            dbc.CardBody([html.H4("Step 2", className="card-title"),
                html.H5(
                    "Choose Range of Years to Search",
                    className="card-text",
                ),
            ])
]

view_output = [
            dbc.CardBody([html.H4("Output", className="card-title"),
                html.H5(
                    "Search Wizard Results",
                    className="card-text",
                ),
            ])
]

your_string = get_text_output()

app.layout = dbc.Container(
    html.Div([
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        dbc.Row(dbc.Card(card_content, color="secondary", inverse=True)),
        dbc.Row(dbc.Card(step_one, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row(
            html.Div([
                dbc.InputGroup([
                    dbc.Input(id='list-in',placeholder='Example ... AFDGRR AFDAPX', type='text'),
                    dbc.Button("Create Product List",id='submit-button', n_clicks=0),
            ], style={'padding':'1em'}),
                html.Div(id='list-out', style={'border': '2px gray solid', 'padding':'1em'},)])
        ),
        dbc.Row(dbc.Card(step_two, color="info", inverse=True), style={'padding':'1em'}),

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
    style={"padding": "1em"},
    ),
        dbc.Row(dbc.Card(view_output, color="success", inverse=True), style={'padding':'1em'}),
        dbc.Row(html.Div(your_string, style={'whiteSpace': 'pre-line', 'border': '2px gray solid', 'padding':'1em'}))

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