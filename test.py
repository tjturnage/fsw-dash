import os
import sys
from datetime import datetime
import dash
from dash import html, dcc

# bootstrap is what helps styling for a better presentation
import dash_bootstrap_components as dbc

# State allows the user to enter input before proceeding
from dash.dependencies import Input, Output,State
import time

# ----------------------------------------
#        Initiate Dash app
# ----------------------------------------

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.DARKLY])
app.title = "Forecast Search Wizard"

# ----------------------------------------
#        Set Slider end year = current year
# ----------------------------------------

now = datetime.utcnow()
this_year = now.year

# next year is needed to bump out slider range to include current year
next_year = this_year + 1

# choose proper host

#FSW_DIR = '/Forecast_Search_Wizard'                            # instance
FSW_DIR = '/home/tjturnage/scripts/Forecast_Search_Wizard'      # pyany
#FSW_DIR = '/data/scripts/Forecast_Search_Wizard'               # tw

DATA_DIR = os.path.join(FSW_DIR, 'TEXT_DATA')
RUN_DIR = os.path.join(FSW_DIR, 'RUN_ME')
FSW_OUTPUT_DIR = os.path.join(FSW_DIR,'FSW_OUTPUT')

try:
    os.chdir(RUN_DIR)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except:
    print("Cant import!")

# ----------------------------------------
#        Set up class then instantiate
# ----------------------------------------
class FSW:
    def __init__(self,word_list=None, product_list=None,start_year=2010,end_year=this_year,isAnd=False,byForecast=True,isGrep=True):
        self.word_list = word_list
        self.product_list = product_list
        self.start_year = start_year
        self.end_year = end_year
        self.isAnd = isAnd
        self.byForecast = byForecast
        self.isGrep = isGrep
        self.made_word_list = False
        self.made_product_list = False
        self.fname = None
        self.fpath = None
        self.original_fpath = None
        self.fpath_contents = None

def new_file_available():
    """
    file listing is now sorted to assure that the newest file is at the end of the list
    There was some weirdness going on where "." and ".." were out of sequence and causing problems
    """
    sa.fname = sorted(os.listdir(FSW_OUTPUT_DIR))[-1]
    this_fpath = os.path.join(FSW_OUTPUT_DIR,sa.fname)
    print(this_fpath)
    if this_fpath != sa.original_fpath:
        print(f"Yay! {this_fpath}")
        sa.fpath = this_fpath
        return True
    else:
        print("Not yet")
        return False

sa = FSW()

# ----------------------------------------
#        Define Webpage variables
# ----------------------------------------

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
            dbc.CardBody([html.H5("Enter Words or Phrases you want to search for, separating each by a comma. Then click button to submit.", 
            className="card-text"),])]

step_two = [
            dbc.CardBody([html.H5("Enter Products in upper case and separated by spaces. Click to create product list.",
            className="card-text"),])]

step_three = [
            dbc.CardBody([html.H5("Choose Range of Years to Search", className="card-text"),])]

step_four = [
            dbc.CardBody([html.H5("Provide Details About How to Search", className="card-text"),])]

view_output = [
            dbc.CardBody([html.H5("Output", className="card-title", style=bold),
                html.P(
                    "Forecast Search Wizard Results",
                    className="card-text",
                ),])]

# ----------------------------------------
#        Build Webpage layout
# ----------------------------------------

app.layout = dbc.Container(
    html.Div([
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        dbc.Row(dbc.Card(top_content, color="secondary", inverse=True)),
        dbc.Row(dbc.Card(step_one, color="info", inverse=True), style={'padding':'1em'}),
        dbc.Row(
            html.Div([
                dbc.InputGroup([
                    dbc.Input(id='input_words_list',placeholder='Example ... SEABREEZE, SEA BREEZE', type='text'),
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

        #############
        # Range Slider
        #############
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
            ]),

        #############
        # Search Methods
        #############    
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
                             {"label": "Part of (like grep)", "value": True},
                             {"label": "Entire", "value": False},
                         ], value=True, style={'padding':'1em'}),
                     html.Div(id="isGrep-out",style=feedback)
                    ])
                ),

        ]),

        #############
        # Check Selections
        #############  
        dbc.Row([
            dbc.Col(
                html.Div([
                dbc.Button("Click Here to Check Selections",id='full_vars', n_clicks=0, style={'padding':'1em','width':'100%'}),
                html.Div(id="full_vars-out",style=feedback)
                ],
                style={'padding':'1em'},

                )
            ),]),

        #############
        # Check Launch Script
        #############  
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Click Here to Launch FSW Script",id='run_script', n_clicks=0, style={'padding':'1em','width':'100%'}),
                    html.Div(children="You'll be notified here when the script completes ...",id="script-status",style=feedback)
                ],
                style={'padding':'1em'}
                )
            ),
        ],style={'padding':'0.5em'}),

        #############
        # View output
        #############
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Show File Content", id="display-file-content-btn", color="success", style={'padding':'1em','width':'100%'}),
                    html.Div(children="File output will display here... ",id="display-file-content-response",style=feedback)
                ],
                style={'padding':'1em'})
            )
        ],style={'padding':'0.5em'}),

        #############
        # Download output
        #############
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button("Download FSW Output File", id="download-btn", color="success", style={'padding':'1em','width':'100%'}),
                    dcc.Download(id="download")
                ],
                style={'padding':'1em'})
            )
        ],style={'padding':'0.5em'}),
    ]),

    ])
)

#mSNu87%H2%2

# ----------------------------------------
#        Data validation, only digits, upper case letters, and commas allowed
# ----------------------------------------
import re
test = '[a-z]|\{|\}|\[|\]|\(|\)|\$|\&|\=|\*|\-|\.|\\|\/'

def regex_test(test_string):
    test = '[a-z]|\{|\}|\[|\]|\(|\)|\$|\&|\=|\*|\-|\.|\\|\/'
    m = re.search(test,test_string)
    # returns True if no disallowed characters are found
    return m is None

# ----------------------------------------
#        Download Setup
# ----------------------------------------

@app.callback(
    Output("download", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True,
)

# func_test is a pretty undescriptive name for what's happening
def func_test(n_clicks):
    return dcc.send_file(
        "/Forecast_Search_Wizard/FSW_OUTPUT/{}".format(sa.fname)
    )


# ----------------------------------------
#        Input words
# ----------------------------------------

# the only data validation being done so far is taking out extra spaces
# much more to do here
@app.callback(Output("input_words_list-out", "children"),
                [Input("input_words_list_submit","n_clicks")],
                [State("input_words_list","value")])
def create_word_list(n_clicks,myvalue):
    original_word_list = sa.word_list
    if n_clicks > 0:
        this_str = str(myvalue)
        if regex_test(this_str):
            fixed_str = this_str.replace(', ',',')
            word_list = fixed_str.split(',')
            if word_list != original_word_list:
                sa.word_list = word_list        
                sa.made_word_list = True
                return str(sa.word_list)
            else:
                return
        else:
            return 'Only upper case letters, digits, and commas allowed!'
    else:
        return

# ----------------------------------------
#        Product list
# ----------------------------------------

# data validation is practically non-existent here
# much more to do
@app.callback(Output("forecast_product_list-out", "children"),
                [Input("forecast_product_list_submit","n_clicks")],
                [State("forecast_product_list","value")])
def create__product_list(n_clicks,myvalue):
    original_product_list = sa.product_list
    if n_clicks > 0:
        input_string = str(myvalue)
        if regex_test(input_string):
            product_list = input_string.split(' ')
            if product_list != original_product_list:
                sa.product_list = product_list
                sa.made_product_list = True
                return str(sa.product_list)
            else:
                return
        else:
            return 'Only upper case letters, digits, and commas allowed!'
    else:
        return

# ----------------------------------------
#        Slider values
# ----------------------------------------
@app.callback(Output("slider_values-out", "children"),
                [Input('slider_values',"value")])
def update_output(value):
    start_year = value[0]
    sa.start_year = start_year
    end_year = value[1]
    sa.end_year = end_year
    return 'start_year = {} ........ end_year = {}'.format(start_year,end_year)

#mSNu87%H2%2

# ----------------------------------------
#        Booleans
# ----------------------------------------

@app.callback(
    Output("isAnd-out", "children"),
    [Input("isAnd", "value"),],)
def on_isand_change(isAnd_value):
    template = "isAnd = {}".format(isAnd_value)
    sa.isAnd = isAnd_value
    return template

@app.callback(
    Output("byForecast-out", "children"),
    [Input("byForecast", "value"),],)
def on_byforecast_change(byForecast_value):
    template = "byForecast = {}".format(byForecast_value)
    sa.byForecast = byForecast_value
    return template

@app.callback(
    Output("isGrep-out", "children"),
    [Input("isGrep", "value"),],)
def on_isgrep_change(isGrep_value):
    template = "isGrep = {}".format(isGrep_value)
    sa.isGrep = isGrep_value
    return template

# ----------------------------------------
#        Summarize arguments
# ----------------------------------------

@app.callback(Output("full_vars-out", "children"),
                [Input("full_vars","n_clicks")],)   
def get_full_vars(n_clicks):
    template = "Word list = {} ... Product list = {} ... start_year = {} ... end_year = {} ... isAnd = {} ... byForecast = {} ... isGrep = {}".format(sa.word_list,
                                                                    sa.product_list,
                                                                    sa.start_year,
                                                                    sa.end_year,sa.isAnd,sa.byForecast,sa.isGrep
)

    return template

# ----------------------------------------
#        Execute and monitor FSW script
# ----------------------------------------

# Here, the word or product lists are converted to a single string with "_" between the elements.
# Then, in the NAMELIST_args.py script, this single string is split by "_" to get back to a list.
# this is the easiest way I know of to pass args that are separated by spaces or commas
def arg_from_list(this_list):
    cmd_str = ''
    for x in this_list:
        fixed = x.replace(' ','_')
        cmd_str = cmd_str + fixed + ' '
    return cmd_str

# this is where the newly created file is copied to output.txt in the assets folder
# I chose this location because people cas access it through the web interface
# I gave this a fixed name because an actual fixed URL address is how I display text in an object element
# here is the line of code that uses the copied file ...
#    return [html.ObjectEl(data="https://fsw.nws.noaa.gov/assets/output.txt")]
# obviously I could make this URL address a variable at some point
def process_text():
    cp_cmd_str = "cp /Forecast_Search_Wizard/FSW_OUTPUT/{0} /Forecast_Search_Wizard/web/fsw-dash/assets/output.txt".format(sa.fname)
    os.system(cp_cmd_str)
    return

# need to update this so if the script is launched again output will return to what it is when n_clicks == 0
@app.callback(Output("script-status", "children"),
                [Input("run_script","n_clicks")],)
def execute_script(n_clicks):
    if n_clicks == 0:
        return "After clicking above, you'll be notified here when the script completes ... "
    if sa.made_product_list and sa.made_word_list:
        new_file = new_file_available()
        words = arg_from_list(sa.word_list)
        prods = arg_from_list(sa.product_list)
        sy = sa.start_year
        ey = sa.end_year
        ia = sa.isAnd
        bf = sa.byForecast
        ig = sa.isGrep
        cmd_str1 = f'cd /Forecast_Search_Wizard/RUN_ME ; python NAMELIST_args.py --word_list {words} '
        cmd_str2 = f'--product_list {prods} --start_year {sy} --end_year {ey} --isAnd {ia} --byForecast {bf} --isGrep {ig}'
        cmd_str = cmd_str1 + cmd_str2
        os.system(cmd_str)
        while new_file is False:
            time.sleep(5)
        else:
            sa.new_file = new_file_available()
            process_text();
            return "Script Completed! Click a link below to show file content or download the file."
    else:
        return "Ensure you've submitted both a word/phrase list and a product list before continuing!"

#mSNu87%H2%2

# ----------------------------------------
#        Show Text output window
# ----------------------------------------
@app.callback(
    Output("display-file-content-response", "children"),
    Input("display-file-content-btn","n_clicks"),
    prevent_initial_call=True,
)
# The html default for object element width is way too small.
# Thus, there is a "assets/object.css" file that overrides the defaults
def show_file_content(n_clicks):
    return [html.ObjectEl(data="https://fsw.nws.noaa.gov/assets/output.txt")]


if __name__ == '__main__':
    app.run_server()