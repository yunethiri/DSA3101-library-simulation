import dash
from dash import dcc, html
import dash_bootstrap_components as dbc  # for styling

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
model_http = "http://localhost:8519"
app.title = 'Occupancy Simulation'

# Define the layout of the simulation page
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Occupancy Simulation', 
                style={'font-family': 'Roboto', 'font-weight': 'bold', 
                       'color': '#003D7C', 'font-size': '50px', 
                       'marginTop': '20px', 'marginRight': '40px', 
                       'display': 'inline-block'}),
        # Return back to main page
        dcc.Link('Back to Main Page', href='/', style={'textDecoration': 'none', 'color': '#fff', 'backgroundColor': '#003D7C', 
                                                       'padding': '6px 12px', 'borderRadius': '5px', 'fontSize': '14px', 
                                                       'display': 'inline-block', 'text-align': 'center'
        })
               ], 
        style={'display': 'flex', 'alignItems': 'flex-end', 'justifyContent': 'flex-start', 'paddingLeft': '20px'}
        ),

    html.H2('Adjust the operating parameters to simulate library occupancy', style={'background-color': '#F8F8F8', 'font-size': '20px',
                                                        'padding-left': '20px','padding-top': '20px', 'padding-bottom': '20px',
                                                        'margin-top': '10px', 'color': '#003D7C'}),
    
    dbc.Container(
        dbc.Row([                
            dbc.Col(html.Div(children=[
                html.H2('Manual', style={'color':'white', 'backgroundColor': '#212529', 
                                                                      'padding': '18px 15px', 
                                                                      'font-size': '18px'}), 
                html.H3(children=[
                    'Press ', html.Strong('RESET'), ' everytime before new simulation', 
                    html.Br(),
                    html.Br(),
                    html.Strong('Start/Stop: '),
                    html.Br(),
                    'Start or stop the simulation at any time for closer investigation',
                    html.Br(),
                    html.Br(),
                    html.Strong('Step: '),
                    html.Br(),
                    'Press to investigate step-by-step',
                    html.Br(),
                    html.Br(),
                    html.Strong('Frames per Second'),
                    html.Br(),
                    'Increases the speed of running the model simulation',
                    html.Br(),
                    html.Br(),
                    html.Strong('Seat Type Slide Bars:'),
                    html.Br(),
                    'Only adjust the number of seats of choosen floor, value of other seats will not affect the simulation.',
                    html.Br(),
                    html.Br(),
                    html.Strong('NOTE: ', style={'color':'red'}),
                    html.Br(),
                    '"Overall Number of Users in the Library" represents the total number of students entering the library throughout the day, not all the users will go to the selected floor, they will be distributed to other floors as well', 
                    ], 
                    style={'font-size': '15px', 'padding': '10px 15px', 'display':'table'}
                    )], 
                    style={'marginRight':'10px', 'marginLeft':'10px', 'border': '1px solid #5F5B5B'}), width=2),

            dbc.Col(html.Iframe(src=model_http, style={'height': '1500px', 'width': '100%'}), width=10),
            ]),
            fluid=True), 
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
