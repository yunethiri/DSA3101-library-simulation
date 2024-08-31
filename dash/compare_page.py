import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import pandas as pd
import plotly.express as px
import requests
import json
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])

app.title = 'Compare Simulations'
# Get the current working directory
current_directory = os.getcwd()

# Define the layout of your web page
app.layout = html.Div([
    html.Div(children=[
        html.H1("Compare Simulations",
                style={'font-family': 'Roboto', 'font-weight': 'bold',
                       'color': '#003D7C', 'font-size': '50px',
                       'marginTop': '20px', 'marginRight': '40px',
                       'display': 'inline-block'}),
        # Return back to the main page
        html.A('Back to Main Page', href='http://localhost:8050', style={'textDecoration': 'none', 'color': '#fff', 'backgroundColor': '#003D7C',
                                                       'padding': '6px 12px', 'borderRadius': '5px', 'fontSize': '14px',
                                                       'display': 'inline-block', 'text-align': 'center'
        })
    ],
    style={'display': 'flex', 'alignItems': 'flex-end', 'justifyContent': 'flex-start', 'paddingLeft': '20px'}
    ),
    html.H2('Multiple simulations for comparison.', style={'background-color': '#F8F8F8', 'font-size': '20px',
                                                        'padding-left': '20px','padding-top': '20px', 'padding-bottom': '20px',
                                                        'margin-top': '10px', 'color': '#003D7C'}),
    
    html.Div([
        # Multi-choice for Level
        html.Label("Select Level in Central Library"),
        dcc.Dropdown(
            id="level-dropdown",
            options=[
                {'label': '3', 'value': 3},
                {'label': '4', 'value': 4},
                {'label': '5', 'value': 5},
                {'label': '6', 'value': 6},
            ],
            value=3,  # Initial value
        ),
    ], style={'width': '48%', 'display': 'inline-block','text-align': 'center', 'margin-left': '25%','margin-bottom': '30px'}),
    
    html.Div([
        # Exam Period Radio Button
        html.Label("Exam Period?"),
        dcc.RadioItems(
            id="exam-radio",
            options=[
                {'label': 'Yes', 'value': 'yes'},
                {'label': 'No', 'value': 'no'},
            ],
            value='yes',  # Initial value
        ),
    ], style={'width': '48%', 'display': 'inline-block','text-align': 'center', 'margin-left': '25%','margin-bottom': '30px'}),

    # Container for dynamically generated sliders
    html.Div(id="sliders-container"),

    # Display the results
    html.Div(id="output3"),
    html.Div(id="output4"),
    html.Div(id="output5"),
    html.Div(id="output6"),
    html.Div(id='graph-output')
])



# Callback to dynamically generate sliders based on the selected level
@app.callback(Output("sliders-container", "children"),
              Input("level-dropdown", "value"))
        
def generate_sliders(level):
    if level == 3:
        sliders = [
            html.Div([
                html.Label("(1)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-1",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),
        
            html.Div([
                html.Label("(2)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-2",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),

            
            html.Div([
                html.Label("(1)Number of seats for discussion cubicles at L3"),
                dcc.Slider(
                    id="discussion-cubicles-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(2)Number of seats for discussion cubicles at L3"),
                dcc.Slider(
                    id="discussion-cubicles-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            
            html.Div([
                html.Label("(1)Number of seats for movable seats at L3"),
                dcc.Slider(
                    id="movable-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(2)Number of seats for movable seats at L3"),
                dcc.Slider(
                    id="movable-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(1)Number of seats for soft seats at L3&L4"),
                dcc.Slider(
                    id="soft-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(2)Number of seats for soft seats at L3&L4"),
                dcc.Slider(
                    id="soft-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(1)Number of seats for sofa at L3&L4"),
                dcc.Slider(
                    id="sofa-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(2)Number of seats for sofa at L3&L4"),
                dcc.Slider(
                    id="sofa-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Button('Submit', id='run-button3', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'}),
            html.Button('See Results', id='results-button', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'})
        ]
    elif level == 4:
        sliders = [
            html.Div([
                html.Label("(1)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-1",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),
        
            html.Div([
                html.Label("(2)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-2",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),

            html.Div([
                html.Label("(1)Number of seats for soft seats at L3&L4"),
                dcc.Slider(
                    id="soft-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(2)Number of seats for soft seats at L3&L4"),
                dcc.Slider(
                    id="soft-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(1)Number of seats for sofa at L3&L4"),
                dcc.Slider(
                    id="sofa-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(2)Number of seats for sofa at L3&L4"),
                dcc.Slider(
                    id="sofa-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Button('Submit', id='run-button4', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'}),
            html.Button('See Results', id='results-button', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'})
        ]
    elif level == 5:
        sliders = [
            html.Div([
                html.Label("(1)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-1",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),
        
            html.Div([
                html.Label("(2)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-2",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),

            html.Div([
                html.Label("(1)Number of seats for windowed seats at L5&L6"),
                dcc.Slider(
                    id="windowed-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(2)Number of seats for windowed seats at L5&L6"),
                dcc.Slider(
                    id="windowed-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(1)Number of seats for 4-man tables at L5"),
                dcc.Slider(
                    id="four-man-tables-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(2)Number of seats for 4-man tables at L5"),
                dcc.Slider(
                    id="four-man-tables-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(1)Number of seats for 8-man tables at L5"),
                dcc.Slider(
                    id="eight-man-tables-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.Label("(2)Number of seats for 8-man tables at L5"),
                dcc.Slider(
                    id="eight-man-tables-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Button('Submit', id='run-button5', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'}),
            html.Button('See Results', id='results-button', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'})
        ]
    elif level == 6:
        sliders = [
            html.Div([
                html.Label("(1)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-1",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),
        
            html.Div([
                html.Label("(2)Number of Students visiting CLB"),
                dcc.Slider(
                    id="students-slider-2",
                    min=0,
                    max=3000,
                    step=50,
                    value=500,  # Initial value
                    marks={i: str(i) for i in range(0, 3001, 200)},
                ),
            ], style={'width': '50%', 'display': 'inline-block', 'margin-bottom': '20px'}),


            html.Div([
                html.Label("(1)Number of seats for windowed seats at L5&L6"),
                dcc.Slider(
                    id="windowed-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(2)Number of seats for windowed seats at L5&L6"),
                dcc.Slider(
                    id="windowed-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(1)Number of seats for diagonal seats at L6"),
                dcc.Slider(
                    id="diagonal-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label("(2)Number of seats for diagonal seats at L6"),
                dcc.Slider(
                    id="diagonal-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("(1)Number of seats for cubicles seats at L6"),
                dcc.Slider(
                    id="cubicles-seats-slider1",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.Label("(2)Number of seats for cubicles seats at L6"),
                dcc.Slider(
                    id="cubicles-seats-slider2",
                    min=0,
                    max=200,
                    step=25,
                    value=100,  # Initial value
                    marks={i: str(i) for i in range(0, 201, 50)},
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Button('Submit', id='run-button6', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'}),
            html.Button('See Results', id='results-button', n_clicks=0, style={'height': '40px', 'width': '150px', 'font-size': '18px', 
                                                                       'padding': '10px', 'margin': '10px'})
        ]

    return sliders

# Update callback to include all sliders in Input
@app.callback(
    Output('output3','children'),
    Input('run-button3', 'n_clicks'),
    [State('level-dropdown', 'value'),
     State('exam-radio', 'value'),
     State('students-slider-1', 'value'),
     State('students-slider-2', 'value'),
     State('discussion-cubicles-slider1', 'value'),
     State('discussion-cubicles-slider2', 'value'),
     State('movable-seats-slider1', 'value'),
     State('movable-seats-slider2', 'value'),
     State('soft-seats-slider1', 'value'),
     State('soft-seats-slider2', 'value'),
     State('sofa-slider1', 'value'),
     State('sofa-slider2', 'value')
     ]
)
def update_run_button(rb,iln,ies,ss1,ss2,dcs1,dcs2,mvs1,mvs2,sss1,sss2,sos1,sos2):
    if rb == 0:
        raise PreventUpdate
    # Create a request to trigger batch run in the model container
    input_params = {
        "input_level_num": iln,
        "input_exam_season": ies,
        "input_users_values": [ss1, ss2],
        "num_seats_discussion_cubicles_values": [dcs1, dcs2],
        "num_seats_moveable_seats_values": [mvs1, mvs2],
        "num_seats_soft_seats_values": [sss1, sss2],
        "num_seats_sofa_values": [sos1, sos2],
    }

    # Convert the dictionary to JSON
    payload = json.dumps(input_params)

    # Make a POST request to the backend API
    response = requests.post('http://endpoints:8520/run_model', json=payload)
    return response.status_code
#add in plot for output

@app.callback(
    Output('output4','children'),
    Input('run-button4', 'n_clicks'),
    [State('level-dropdown', 'value'),
     State('exam-radio', 'value'),
     State('students-slider-1', 'value'),
     State('students-slider-2', 'value'),
     State('soft-seats-slider1', 'value'),
     State('soft-seats-slider2', 'value'),
     State('sofa-slider1', 'value'),
     State('sofa-slider2', 'value')
     ]
)
def update_run_button4(rb,iln,ies,ss1,ss2,sss1,sss2,sos1,sos2):
    if rb == 0:
        raise PreventUpdate
    # Create a request to trigger batch run in the model container
    if iln == 4:    
        input_params = {
            "input_level_num": iln,
            "input_exam_season": ies,
            "input_users_values": [ss1, ss2],
            "num_seats_soft_seats_values": [sss1, sss2],
            "num_seats_sofa_values": [sos1, sos2],
        }

        # Convert the dictionary to JSON
        payload = json.dumps(input_params)

        # Make a POST request to the backend API
        response = requests.post('http://endpoints:8520/run_model4', json=payload)
        return response.status_code
  
@app.callback(
    Output('output5','children'),
    Input('run-button5', 'n_clicks'),
    [State('level-dropdown', 'value'),
     State('exam-radio', 'value'),
     State('students-slider-1', 'value'),
     State('students-slider-2', 'value'),
     State('windowed-seats-slider1', 'value'),
     State('windowed-seats-slider2', 'value'),
     State('four-man-tables-slider1', 'value'),
     State('four-man-tables-slider2', 'value'),
     State('eight-man-tables-slider1', 'value'),
     State('eight-man-tables-slider2', 'value')
     ]
)
def update_run_button5(rb,iln,ies,ss1,ss2,wss1,wss2,fmt1,fmt2,emt1,emt2):
    if rb == 0:
        raise PreventUpdate
    # Create a request to trigger batch run in the model container
    if iln == 5:    
        input_params = {
            "input_level_num": iln,
            "input_exam_season": ies,
            "input_users_values": [ss1, ss2],
            "num_seats_windowed_values": [wss1, wss2],
            "num_seats_4": [fmt1, fmt2],
            "num_seats_8": [emt1, emt2]
        }

        # Convert the dictionary to JSON
        payload = json.dumps(input_params)

        # Make a POST request to the backend API
        response = requests.post('http://endpoints:8520/run_model5', json=payload)
        return response.status_code
    
@app.callback(
    Output('output6','children'),
    Input('run-button6', 'n_clicks'),
    [State('level-dropdown', 'value'),
     State('exam-radio', 'value'),
     State('students-slider-1', 'value'),
     State('students-slider-2', 'value'),
     State('windowed-seats-slider1', 'value'),
     State('windowed-seats-slider2', 'value'),
     State('diagonal-seats-slider1', 'value'),
     State('diagonal-seats-slider2', 'value'),
     State('cubicles-seats-slider1', 'value'),
     State('cubicles-seats-slider2', 'value')
     ]
)
def update_run_button6(rb,iln,ies,ss1,ss2,wss1,wss2,dss1,dss2,css1,css2):
    if rb == 0:
        raise PreventUpdate
    if iln == 6:
        # Create a request to trigger batch run in the model container
        input_params = {
            "input_level_num": iln,
            "input_exam_season": ies,
            "input_users_values": [ss1, ss2],
            "num_seats_window": [wss1, wss2],
            "num_seats_diagonal": [dss1, dss2],
            "num_seats_cubicles": [css1, css2]
        }

        # Convert the dictionary to JSON
        payload = json.dumps(input_params)

        # Make a POST request to the backend API
        response = requests.post('http://endpoints:8520/run_model6', json=payload)
        return response.status_code

@app.callback(
    Output('graph-output', 'children'),
    Input('results-button', 'n_clicks'))
def update_graph(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    
    filepath = "./results/results_for_specific_combinations.csv"
    if not os.path.exists(filepath):
        return "File not found. Please run the simulation first."

    df = pd.read_csv(filepath)
    def create_figure_num(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['time'], y=data['current_num_users_on_floor'], mode='lines', name='Current of Number Users on Floor'))
        fig.add_trace(go.Scatter(x=data['time'], y=data['current_num_users_unable_to_find_seat'], mode='lines', name='Current Number of Users Unable to Find Seat'))
        fig.add_trace(go.Scatter(x=data['time'], y=data['current_num_users_didnt_get_preferred_seat'], mode='lines', name="Current Number of Users didn't Get Preferred Seat"))
        fig.add_trace(go.Scatter(x=data['time'], y=data['current_num_seats_choped'], mode='lines', name='Current Number of Seats Choped'))
        fig.update_layout(xaxis_title='Time', yaxis_title='Values')
        return fig
    
    def create_figure_num_rate(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['time'], y=data['satisfaction_rate'], mode='lines', name='Current User Satisfaction Rate'))
        fig.add_trace(go.Scatter(x=data['time'], y=data['occupancy_rate(level)'], mode='lines', name='Current Floor Occupancy Rate'))
        fig.update_layout(xaxis_title='Time', yaxis_title='Rate')
        return fig

    mid_index = len(df) // 2
    first_half = df.iloc[:mid_index]
    second_half = df.iloc[mid_index:]

    fig1 = create_figure_num(first_half)
    fig2 = create_figure_num(second_half)
    fig3 = create_figure_num_rate(first_half)
    fig4 = create_figure_num_rate(second_half)

    return html.Div([
        # First row with two graphs
        html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ], style={'display': 'flex', 'justify-content': 'space-around'}),

        # Second row with two graphs
        html.Div([
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4)
        ], style={'display': 'flex', 'justify-content': 'space-around'})
    ], style={'display': 'flex', 'flex-direction': 'column'})



if __name__ == '__main__':
    app.run_server(debug=True, port=8052, host='0.0.0.0',)
