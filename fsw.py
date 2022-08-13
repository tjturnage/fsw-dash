from datetime import datetime
from gc import callbacks
import numpy as np


#import re
from textwrap import wrap
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import pandas as pd
#import glob
import os

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.DARKLY])#, 'https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = "Forecast Search Wizard"

now = datetime.utcnow()
this_year = now.year
next_year = this_year + 1

try:
    os.listdir('/data/')
    root_dir = '/data'
    FSW_DIR = '/Forecast_Search_Wizard'
    DATA_DIR = os.path.join(root_dir, 'TEXT_DATA')
    print(DATA_DIR)
    FSW_OUTPUT_DIR = os.path.join(FSW_DIR,'FSW_OUTPUT')

except:
    root_dir = 'C:/data/'
    #root_dir = '/home/tjturnage/'



#your_string = get_text_output()

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
                dbc.CardLink("@ForecastWizard", href="https://github.com/allenea/Forecast_Search_Wizard"),
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
                max=this_year,
                value=[2010, 2020],
                marks={i: str(i) for i in range(1996,next_year)},
                )
            )
    ],
    style={"padding": "1em"},
    ),
        dbc.Row(dbc.Card(view_output, color="success", inverse=True), style={'padding':'1em'}),
        dbc.Row(dbc.Button("Click to Toggle Text On/Off",id="refresh-text", n_clicks=0), style={'padding':'1em'}),
        dbc.Row(html.Div(children=" ", id="new-text", style={'whiteSpace': 'pre-line', 'border': '2px gray solid', 'padding':'1em'}))

    ])
)


@app.callback(Output(component_id='list-out', component_property='children'),
                [Input(component_id='submit-button',component_property='n_clicks')],
                [State('list-in','value')])
def create_list(n_clicks,myvalue):
    input_string = str(myvalue)
    product_list = input_string.split(' ')
    return str(product_list)

@app.callback(Output(component_id='new-text', component_property='children'),
                [Input(component_id='refresh-text',component_property='n_clicks')],)
def get_text_output(n_clicks):
    fname = os.listdir(FSW_OUTPUT_DIR)[-1]
    text_file_path = os.path.join(FSW_OUTPUT_DIR,fname)
    fin = open(text_file_path, 'r')
    text_data = fin.read()
    fin.close()
    make_dataframe(text_data)

    if n_clicks%2 == 0:
        return text_data
    else:
        return ""

def make_dataframe(text):
    dts = []
    product = []
    lines = text.splitlines()
    for line in lines:
        if line[0] in ('0','1'):
            values = line.split('\t')
            dts.append(values[0])
            product.append(values[1][1:])


    dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
    data = {'dts':dts_pd, 'product':product}
    df_full = pd.DataFrame(data)
    df_full.set_index('dts', inplace=True)
    df = df_full[df_full['product'] == 'AFDGRR']
    monthly = df.resample('M').count()
    #print(monthly)
    x=df.index
    y=monthly['product']
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.show()
    return

if __name__ == '__main__':
    app.run_server()