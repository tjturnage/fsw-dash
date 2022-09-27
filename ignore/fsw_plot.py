#############################################
### This file is not currently being used ###
#############################################

from dash import Dash, Input, Output, callback, dash_table,html,dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime
# -------------------------------------------------------------------------------------

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

    #print(df_full)
    return df_full

# ----------------------------------------
### Pandas stuff
# ----------------------------------------

def make_dataframe():
    fin = open('/home/thomas.turnage/scripts/fsw-dash/assets/output.txt', 'r')
    text = fin.read()
    fin.close()
    dts = []
    product = []
    lines = text.splitlines()
    for line in lines:
        if len(line) > 0:
            if line[0] in ('0','1'):
                values = line.split('\t')
                dts.append(values[0])
                product.append(values[1][1:])


    dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
    data = {'dts':dts_pd, 'product':product}
    df_full = pd.DataFrame(data)
    df_full.set_index('dts', inplace=True)
    monthly = df_full.resample('M').count()
    print(monthly)
    #x=df.index
    #y=monthly['product']
    #fig = go.Figure(data=go.Scatter(x=x, y=y))
    #fig.show()
    return df_full

def make_dataframe():
    #fin = open('/home/thomas.turnage/scripts/fsw-dash/assets/output.txt', 'r')
    fin = open('C:/data/scripts/dash-data/test.txt', 'r')
    text = fin.read()
    fin.close()
    dts = []
    product = []
    office = []
    lines = text.splitlines()
    for line in lines:
        if len(line) > 0:
            if line[0] in ('0','1'):
                values = line.split('\t')
                dts.append(values[0])
                product.append(values[1][1:4])
                office.append(values[1][4:])

    dts_pd = pd.to_datetime(dts,infer_datetime_format=True)
    data = {'dts':dts_pd, 'product':product, 'office':office}
    df = pd.DataFrame(data)
    df.set_index(['dts'], inplace=True)
    df['id'] = df.index.strftime('%Y%m%d%H%M')
    df['year'] = df.index.year
    df['hour'] = df.index.hour
    df['month'] = df.index.month

    #df.astype({'year': 'int64','hour':'int64','month':'int64'}).dtypes
    #df.astype({'id':'object'}).dtypes
    return df

df = make_dataframe();
#print(df)
df.to_csv('test.csv')
df.set_index('id', inplace=True, drop=False)
#print(df.columns)

# -------------------------------------------------------------------------------------
# App layout
app = Dash(__name__, prevent_initial_callbacks=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sorting operators (https://dash.plotly.com/datatable/filtering)

def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        return 'any'

app.layout = dash_table.DataTable(
    #columns=[
    #    {'name': i, 'id': i, 'type': table_type(df[i])} for i in df.columns
    #],
    columns=[
        {'name': 'DateTime', 'id': 'dts', 'type': 'datetime'},
        {'name':'id', 'id': 'product', 'type': 'text'},
        {'name': 'Office', 'id': 'office', 'type': 'text'},
        {'name': 'Month', 'id': 'month', 'type': 'numeric'},
        {'name': 'ID', 'id':'id', 'type': 'text'},
        {'name': 'Hour', 'id': 'hour', 'type': 'numeric'},
        {'name': 'Year', 'id': 'year', 'type': 'numeric'},
    ],
    data=df.to_dict('records'),
    filter_action='native',

    css=[{
        'selector': 'table',
        'rule': 'table-layout: fixed'  # note - this does not work with fixed_rows
    }],
    style_table={'height': 400},
    style_data={
        'width': '{}%'.format(80. / len(df.columns)),
        'textOverflow': 'hidden'
    }
)

# app.layout = html.Div([
#     dash_table.DataTable(
#         id='datatable-interactivity',
#         columns=[
#             {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
#             for i in df.columns
#         ],
#         # columns=[
#         #     {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
#         #     for i in df.columns
#         # ],
#         data=df.to_dict('records'),  # the contents of the table
#         #editable=False,              # allow editing of data inside all cells
#         filter_action="native",     # allow filtering of data by user ('native') or not ('none')
#         sort_action="native",       # enables data to be sorted per-column by user or not ('none')
#         #sort_mode="multi",         # sort across 'multi' or 'single' columns
#         #column_selectable="multi",  # allow users to select 'multi' or 'single' columns
#         #row_selectable="multi",     # allow users to select 'multi' or 'single' rows
#         row_deletable=False,         # choose if user can delete a row (True) or not (False)
#         selected_columns=[],        # ids of columns that user selects
#         selected_rows=[],           # indices of rows that user selects
#         page_action="native",       # all data is passed to the table up-front or not ('none')
#         page_current=0,             # page number that user is on
#         page_size=30,                # number of rows visible per page
#         style_cell={                # ensure adequate header width when text is shorter than cell's text
#             'minWidth': '150px', 'maxWidth': '150px', 'width': '150px'
#         },
#         style_cell_conditional=[    # align text columns to left. By default they are aligned to right
#             {
#                 'if': {'column_id': c},
#                 'textAlign': 'left'
#             } for c in ['product', 'office']
#         ],
#         style_data={                # overflow cells' content into multiple lines
#             'whiteSpace': 'normal',
#             'height': 'auto'
#         }
#     ),

#     html.Br(),
#     html.Br(),
#     html.Div(id='bar-container'),
#     html.Div(id='choromap-container')

# ])


# #-------------------------------------------------------------------------------------
# #Create bar chart
# @app.callback(
#     Output(component_id='bar-container', component_property='children'),
#     [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
#      Input(component_id='datatable-interactivity', component_property='selected_rows'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
#      Input(component_id='datatable-interactivity', component_property='active_cell'),
#      Input(component_id='datatable-interactivity', component_property='selected_cells')]
# )
# def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
#                order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
#     print('***************************************************************************')
#     print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
#     print('---------------------------------------------')
#     print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
#     print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
#     print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
#     print('---------------------------------------------')
#     print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
#     print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
#     print("---------------------------------------------")
#     print("Complete data of active cell: {}".format(actv_cell))
#     print("Complete data of all selected cells: {}".format(slctd_cell))

#     dff = pd.DataFrame(all_rows_data)

#     # used to highlight selected countries on bar chart
#     colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
#               for i in range(len(dff))]

#     if "product" in dff and "id" in dff:
#         return [
#             dcc.Graph(id='bar-chart',
#                       figure=px.bar(
#                           data_frame=dff,
#                           x="id",
#                           y='product',
#                           labels={"did online course": "% of Pop took online course"}
#                       ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
#                       .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
#                       )
#         ]


# -------------------------------------------------------------------------------------
# Create choropleth map
# @app.callback(
#     Output(component_id='choromap-container', component_property='children'),
#     [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
#      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows')]
# )
# def update_map(all_rows_data, slctd_row_indices):
#     dff = pd.DataFrame(all_rows_data)

#     # highlight selected countries on map
#     borders = [5 if i in slctd_row_indices else 1
#                for i in range(len(dff))]

#     if "iso_alpha3" in dff and "internet daily" in dff and "country" in dff:
#         return [
#             dcc.Graph(id='choropleth',
#                       style={'height': 700},
#                       figure=px.choropleth(
#                           data_frame=dff,
#                           locations="iso_alpha3",
#                           scope="europe",
#                           color="internet daily",
#                           title="% of Pop that Uses Internet Daily",
#                           template='plotly_dark',
#                           hover_data=['country', 'internet daily'],
#                       ).update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
#                       .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
#                                                                               "%{customdata[1]}" + "%")
#                       )
#         ]


# -------------------------------------------------------------------------------------
# Highlight selected column
#@app.callback(
#    Output('datatable-interactivity', 'style_data_conditional'),
#    [Input('datatable-interactivity', 'selected_columns')]
#)
#def update_styles(selected_columns):
#    return [{
#        'if': {'column_id': i},
#        'background_color': '#D2F3FF'
#    } for i in selected_columns]


# -------------------------------------------------------------------------------------






if __name__ == '__main__':
    app.run_server(debug=True)
    
    
# https://youtu.be/USTqY4gH_VM
    

