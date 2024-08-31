import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from simulation_page import app as simulation_app
from summary_page import app as summary_app
from compare_page import app as compare_app
from floor_plan import app as floorplan_app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])
app.title = 'Central Library Occupancy Simulation System'
main_page_layout = html.Div([
    html.Div(children=[
        dbc.Row([
            dbc.Col(html.Img(src=dash.get_asset_url('nus_logo.jpg'), height='120px'), width='auto'),
            dbc.Col(html.H1('Central Library Occupancy Simulation System', 
                            style={'font-family': 'Roboto', 'font-weight': 'bold', 
                                   'color': '#003D7C', 'font-size': '50px',
                                   'marginTop': '20px'})),
        ])
    ]),

    html.Div(children=[
        html.H2(children=[
            html.Strong('Click on the buttons below to go to the webpage')
        ]),
    ], style={'background-color': '#F8F8F8', 'font-size': '20px',
              'padding-left': '40px','padding-top': '20px', 'padding-bottom': '20px',
              'margin-top': '20px', 'color': '#003D7C'}),

    html.Div([
        html.Div([
            dcc.Link(html.Button([html.Img(src=dash.get_asset_url('summary-button.png'), style={'width': '150px', 'height': '150px', 'position': 'absolute', 
                                                                                                'left': '5%', 'top': '50%', 'transform': 'translateY(-50%)'}),
                                html.Span('User Behaviour Summary', style={'position': 'absolute', 'top': '5%', 'right': '5%', 'color': 'white', 
                                                            'font-size': '25px', 'font-weight': 'bold', 'text-align':'center'}),
                                html.Span('General behaviours of students, based on\
                                          survey data, regarding the current state of the library.', 
                                          style={'position': 'absolute', 'top': '20%', 'left': '55%', 'right': '5%', 'color': 'white', 
                                                 'font-size': '16px', 'text-align':'left', 'paddingTop': '10px'})],
                                id='summary-button',
                                style={'background-color': '#E97A03', 'borderRadius': '10px', 
                                        'padding': '150px 210px', 'border': 'none', 
                                        'margin': '60px 100px 30px 100px', 'position': 'relative'}), 
                                        href='/summary', target="_blank"), 
            html.A(html.Button([html.Img(src=dash.get_asset_url('floor-plan.png'), style={'width': '150px', 'height': '150px', 'position': 'absolute', 
                                                                                                'left': '5%', 'top': '50%', 'transform': 'translateY(-50%)'}),
                                html.Span('Floor Plan', style={'position': 'absolute', 'top': '5%', 'right': '15%', 'color': 'white', 
                                                             'font-size': '25px', 'font-weight': 'bold', 'text-align':'center'}), 
                                html.Span('Detailed floor plan of Central Library from level 3 to 6, contains potentially useful information for your reference.', 
                                          style={'position': 'absolute', 'top': '20%', 'left': '55%', 'right': '5%', 'color': 'white', 
                                                 'font-size': '16px', 'text-align':'left', 'paddingTop': '10px'})],
                                id='about-button', 
                                style={'background-color': '#E97A03', 'borderRadius': '10px', 
                                        'padding': '150px 210px', 'border': 'none', 
                                        'margin': '60px 100px 30px 100px', 'position': 'relative'}), 
                                        href='http://localhost:8051', target="_blank")],
                style={'display': 'flex', 'justifyContent': 'center'}),
        html.Div([
            dcc.Link(html.Button([html.Img(src=dash.get_asset_url('simulation-button.png'), style={'width': '150px', 'height': '150px', 'position': 'absolute', 
                                                                                                'left': '5%', 'top': '50%', 'transform': 'translateY(-50%)'}),
                                html.Span('Model Simulation', style={'position': 'absolute', 'top': '5%', 'right': '5%', 'color': 'white', 
                                                                         'font-size': '25px', 'font-weight': 'bold', 'text-align':'center'}), 
                                html.Span('Input parameters to simulate library occupancy in various scenarios.', 
                                          style={'position': 'absolute', 'top': '20%', 'left': '55%', 'right': '5%', 'color': 'white', 
                                                 'font-size': '16px', 'text-align':'left', 'paddingTop': '10px'})], 
                                id='simulation-button', 
                                style={'background-color': '#E97A03', 'borderRadius': '10px', 
                                        'padding': '150px 210px', 'border': 'none', 
                                        'margin': '30px 100px 60px 100px', 'position': 'relative'}), 
                                        href='/simulation'),
            html.A(html.Button([html.Img(src=dash.get_asset_url('compare-button.png'), style={'width': '150px', 'height': '150px', 'position': 'absolute', 
                                                                                                'left': '5%', 'top': '50%', 'transform': 'translateY(-50%)'}),
                                html.Span('Comparing Simulations', style={'position': 'absolute', 'top': '5%', 'right': '5%', 'color': 'white', 
                                                                        'font-size': '25px', 'font-weight': 'bold', 'text-align':'center'}), 
                                html.Span('Run multiple simulations together with different sets of input\
                                           and compare overall outcomes of different simulations.', 
                                          style={'position': 'absolute', 'top': '20%', 'left': '55%', 'right': '5%', 'color': 'white', 
                                                 'font-size': '16px', 'text-align':'left', 'paddingTop': '10px'})], 
                                id='compare-button', 
                                style={'background-color': '#E97A03', 'borderRadius': '10px', 
                                        'padding': '150px 210px', 'border': 'none', 
                                        'margin': '30px 100px 60px 100px', 'position': 'relative'}), 
                                        href='http://localhost:8052')],
                style={'display': 'flex', 'justifyContent': 'center'})],
    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/summary':
        return summary_app.layout
    elif pathname == '/simulation':
        return simulation_app.layout
    elif pathname == '/compare':
        return compare_app.layout
    elif pathname == '/floor-plan':
        return floorplan_app.layout
    else:
        return main_page_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
