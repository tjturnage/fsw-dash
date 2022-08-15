from datetime import datetime
import numpy as np
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

def get_text_product():
    fname = os.listdir(FSW_OUTPUT_DIR)[-1]
    text_file_path = os.path.join(FSW_OUTPUT_DIR,fname)
    fin = open(text_file_path, 'r')
    text_data = fin.read()
    fin.close()
    return text_data

def make_dataframe(text_data):
    lines = text_data.split('\n')
    dts = []
    product = []
    for i, line in enumerate(lines):
        if len(line) > 10 and line[0] in ('0','1'):
            if i%500 == 0:
                print(f'{i} out of {len(lines)}')
            values = line.split('\t')
            dts.append(values[0])
            product.append(values[1][1:])
            dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
            data = {'dts':dts_pd, 'product':product}
            df_full = pd.DataFrame(data)
            df_full.set_index('dts', inplace=True)
            #df = df_full[df_full['product'] == 'AFDGRR']

    #print(df_full)
    return df_full

try:
    text_data = get_text_product()
    #df = make_dataframe(text_data)
except:
    text_data = "not on instance!"


bold = {'font-weight': 'bold'}
feedback = {'border': '2px gray solid', 'padding':'1em'}

top_content = [
            dbc.CardBody([html.H1("Forecast Search Wizard", className="card-title",style={'font-weight': 'bold', 'font-style': 'italic'}),
                html.H4(
                    "An application to search National Weather Service Text Products by keywords",
                    className="card-text", style={'color':'rgb(52,152,219)', 'font-weight': 'bold', 'font-style': 'italic'}
                ),
                html.H5(
                    "Developed by Eric Allen (eric.allen@noaa.gov)",
                    className="card-text",
                ),
                html.Div([
                dbc.CardLink("GitHub", href="https://github.com/allenea/Forecast_Search_Wizard")]),
                html.Div([
                dbc.CardLink("@WxSearchWizard", href="https://twitter.com/WxSearchWizard")]),])
]

step_one = [
            dbc.CardBody([html.H5("Step 1", className="card-title",style=bold),
                html.P(
                    "Enter Words or phrases you want to search for. This needs to be in a list format.",
                    className="card-text",
                ),
            ])
]

step_two = [
            dbc.CardBody([html.H5("Step 2", className="card-title",style=bold),
                html.P(
                    "Enter Products in upper case and separated by spaces. Click to create product list.",
                    className="card-text",
                ),
            ])
]

step_three = [
            dbc.CardBody([html.H5("Step 3", className="card-title",style=bold),
                html.P(
                    "Choose Range of Years to Search",
                    className="card-text",
                ),
            ])
]

step_four = [
            dbc.CardBody([html.H5("Step 4", className="card-title",style=bold),
                html.P(
                    "Provide Details About How to Search",
                    className="card-text",
                ),
            ])
]

view_output = [
            dbc.CardBody([html.H5("Output", className="card-title", style=bold),
                html.P(
                    "Forecast Search Wizard Results",
                    className="card-text",
                ),
            ])
]

class FSW:
    def __init__(self,input_word_list=['LAKE'], forecast_product_list=['AFDGRR'],start_year=2010,end_year=this_year,isAnd=False,byForecast=True,isGrep=True):
        self.input_word_list = input_word_list
        self.forecast_product_list = forecast_product_list
        self.start_year = start_year
        self.end_year = end_year
        self.isAnd = isAnd
        self.byForecast = byForecast
        self.isGrep = isGrep

script_args = FSW()

app.layout = dbc.Container(
    html.Div([
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        dbc.Row(dbc.Card(top_content, color="secondary", inverse=True)),
        dbc.Row(dbc.Card(step_one, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row(
            html.Div([
                dbc.InputGroup([
                    dbc.Input(id='input_words_list',placeholder='Example ... ["SEA BREEZE", "SEABREEZE"]', type='text'),
                    dbc.Button("Submit Input Words",id='input_words_list_submit', n_clicks=0),
            ], style={'padding':'1em'}),
                html.Div(id='input_words_list-out', style=feedback,)])
        ),
        dbc.Row(dbc.Card(step_two, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row(
            html.Div([
                dbc.InputGroup([
                    dbc.Input(id='forecast_product_list',placeholder='Example ... AFDGRR AFDAPX', type='text'),
                    dbc.Button("Create Product List",id='forecast_product_list_submit', n_clicks=0),
            ], style={'padding':'1em'}),
                html.Div(id='forecast_product_list-out', style=feedback,)])
        ),
        dbc.Row(dbc.Card(step_three, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row([
            html.Div([
                dbc.Col(
                    dcc.RangeSlider(
                    id="slider_values",
                    min=1996,
                    max=this_year,
                    step=1,
                    value=[2010, 2020],
                    marks={i: str(i) for i in range(1996,next_year)},
                    ),style={'padding':'1.2em'},
            ),
            html.Div(id='slider_values-out', style=feedback,)

    ])
    
    ],
    style={"padding": "1em"},
    
    ),
        dbc.Row(dbc.Card(step_four, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Search for { ... } of the words"),
                        dbc.RadioItems(id="isAnd",
                        options=[
                            {"label": "All", "value": True},
                            {"label": "Any", "value": False},
                        ], value=True, style={'padding':'1em'}),
                    html.Div(id="isAnd-out",style=feedback)
                ])
            ),

            dbc.Col(
                html.Div([
                    html.H5("Search by { ... } "),
                        dbc.RadioItems(id="byForecast",
                        options=[
                            {"label": "Forecast", "value": True},
                            {"label": "Day", "value": False},
                        ], value=True, style={'padding':'1em'}),
                    html.Div(id="byForecast-out",style=feedback)
                ])
            ),

            dbc.Col(
                html.Div([
                    html.H5("Search for { ... } word or phrase"),
                        dbc.RadioItems(id="isGrep",
                        options=[
                            {"label": "Part of (like GREP)", "value": True},
                            {"label": "Entire", "value": False},
                        ], value=True, style={'padding':'1em'}),
                    html.Div(id="isGrep-out",style=feedback)
                ])
            ),        
        ]),
        dbc.Row(dbc.Card(view_output, color="success", inverse=True), style={'padding':'1em'}),
        dbc.Row(dbc.Button("Click to Toggle Text Display (could take several seconds to load)",id="refresh-text", n_clicks=0), style={'padding':'1em'}),
        dbc.Row(html.Div(children=" ", id="new-text", style={'whiteSpace': 'pre-line', 'border': '2px gray solid', 'padding':'1em'}))

    ])
)

# input words
@app.callback(Output("input_words_list-out", "children"),
                [Input("input_words_list_submit","n_clicks")],
                [State("input_words_list","value")])
def create_list(n_clicks,myvalue):
    input_string = str(myvalue)
    script_args.input_word_list = input_string
    return str(input_string)

# product list
@app.callback(Output("forecast_product_list-out", "children"),
                [Input("forecast_product_list_submit","n_clicks")],
                [State("forecast_product_list","value")])
def create_list(n_clicks,myvalue):
    input_string = str(myvalue)
    product_list = input_string.split(' ')
    script_args.input_word_list = product_list
    return str(product_list)

# slider values
@app.callback(Output("slider_values-out", "children"),
                [Input('slider_values',"value")])
def update_output(value):
    start_year = value[0]
    script_args.start_year = start_year
    end_year = value[1]
    script_args.end_year = end_year
    return 'start_year = {} ........ end_year = {}'.format(start_year,end_year)

@app.callback(
    Output("isAnd-out", "children"),
    [Input("isAnd", "value"),],)
def on_form_change(isAnd_value):
    template = "isAnd = {}".format(isAnd_value)
    script_args.isAnd = isAnd_value
    return template

@app.callback(
    Output("byForecast-out", "children"),
    [Input("byForecast", "value"),],)
def on_form_change(byForecast_value):
    template = "byForecast = {}".format(byForecast_value)
    script_args.byForecast = byForecast_value
    return template

@app.callback(
    Output("isGrep-out", "children"),
    [Input("isGrep", "value"),],)
def on_form_change(isGrep_value):
    template = "isGrep = {}".format(isGrep_value)
    script_args.isGrep = isGrep_value
    return template

@app.callback(Output("new-text", "children"),
                [Input("refresh-text","n_clicks")],)
def get_text_output(n_clicks):
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

#@app.callback(Output("slider_values-out", "children"),
#                [Input('slider_values',"value")])
#def display_arguments():
#    template = "{} {} {} {}".format(script_args.script_args.isGrep,script_args.start_year)
#    print(template)
#    return


#    dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
#    data = {'dts':dts_pd, 'product':product}
#    df_full = pd.DataFrame(data)
#    df_full.set_index('dts', inplace=True)
#    df = df_full[df_full['product'] == 'AFDGRR']
#    monthly = df.resample('M').count()
#    #print(monthly)
#    x=df.index
#    y=monthly['product']
#    fig = go.Figure(data=go.Scatter(x=x, y=y))
#    fig.show()


if __name__ == '__main__':
    app.run_server()