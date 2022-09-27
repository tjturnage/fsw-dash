import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# ----------------------------------------
#        Initiate Dash app
# ----------------------------------------

app = dash.Dash(__name__, use_pages=True, external_stylesheets= [dbc.themes.DARKLY])
app.title = "Forecast Search Wizard"

bold = {'font-weight': 'bold'}
feedback = {'border': '2px gray solid', 'padding':'1em'}

top_content = dbc.Container([dbc.Container([
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
            ])])

sidebar = dbc.Container([dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page['name'], className='ms-2'),
            ],
            href=page["path"],
            active="exact"
        )
        for page in dash.page_registry.values()
    ],vertical=False,
    pills=True,
    className="bg-dark"
)])

app.layout = dbc.Container([
        dbc.Row([dbc.Col([sidebar],),
        dbc.Row(dbc.Col(html.Div(html.Hr()))),
        dbc.Row(dbc.Col(dbc.Card(top_content, color="secondary", inverse=True))),
        ]),
    
    dbc.Row([dbc.Col([dash.page_container],)]),
    

], fluid=True)

if __name__ == '__main__':
    app.run_server(debug="True")