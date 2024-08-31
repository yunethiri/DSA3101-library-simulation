# Import packages
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

floor_plan_diagrams = {
    'Floor 3' : 'assets/Floor3.png',
    'Floor 4' : 'assets/Floor4.png',
    'Floor 5' : 'assets/Floor5.png',
    'Floor 6' : 'assets/Floor6.png',
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])
app.title = 'Floor Plan'
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Floor plan', 
                style={'font-family': 'Roboto', 'font-weight': 'bold', 
                       'color': '#003D7C', 'font-size': '50px', 
                       'marginTop': '20px', 'marginRight': '40px', 
                       'display': 'inline-block'}),

        html.A('Back to Main Page', href='http://localhost:8050', style={'textDecoration': 'none', 'color': '#fff', 'backgroundColor': '#003D7C', 
                                                       'padding': '6px 12px', 'borderRadius': '5px', 'fontSize': '14px', 
                                                       'display': 'inline-block', 'text-align': 'center'
        })], 
        style={'display': 'flex', 'alignItems': 'flex-end', 'justifyContent': 'flex-start', 'paddingLeft': '20px'}
    ),
    html.H2('Central Library floor plan for reference', style={'background-color': '#F8F8F8', 'font-size': '20px',
                                                        'padding-left': '20px','padding-top': '20px', 'padding-bottom': '20px',
                                                        'margin-top': '10px', 'color': '#003D7C'}),
    html.Div(
        children=[
            html.Label('Please choose a floor', style={'font-size': '20px'}),
            html.Br(),
            dcc.Dropdown(
                id='floor-dropdown',
                options=[{'label': floor, 'value': floor} for floor in floor_plan_diagrams.keys()],
                value='Floor 3',  # Default selected floor
                style={'width': '50%', 'margin': 'auto'},
            ),
            html.Div(id='floor-plan-image-container'),
        ],
        style={'text-align': 'center', 'margin-top': '20px'}  
    ),
])

@app.callback(
    Output('floor-plan-image-container', 'children'),
    Input('floor-dropdown', 'value')
)
def update_floor_plan(selected_floor):
    # Get the image path for the selected floor
    image_path = floor_plan_diagrams[selected_floor]
    #print(f"Selected Floor: {selected_floor}")
    #print(f"Image Path: {image_path}")
    # Display the image using Dash HTML component
    return html.Img(src=image_path, style={'width': '100%', 'height': 'auto'})

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')











