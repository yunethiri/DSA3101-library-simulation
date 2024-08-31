# Import packages
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def make_break(num_breaks):
    br_list = [html.Br()] * num_breaks
    return br_list

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'])
app.title = 'Survey Summary'
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Survey Summary', 
                style={'font-family': 'Roboto', 'font-weight': 'bold', 
                       'color': '#003D7C', 'font-size': '50px', 
                       'marginTop': '20px', 'marginRight': '40px', 
                       'display': 'inline-block'}),

        # Return back to main page
        dcc.Link('Back to Main Page', href='/', style={'textDecoration': 'none', 'color': '#fff', 'backgroundColor': '#003D7C', 
                                                       'padding': '6px 12px', 'borderRadius': '5px', 'fontSize': '14px', 
                                                       'display': 'inline-block', 'text-align': 'center'
        })
        #html.A('Back to Main Page', 
               #style={'display': 'inline-block'},
               #href='/')
               ], 
        style={'display': 'flex', 'alignItems': 'flex-end', 'justifyContent': 'flex-start', 'paddingLeft': '20px'}
        ),
    html.H2('General behaviour of students in Central Library for reference', style={'background-color': '#F8F8F8', 'font-size': '20px',
                                                        'padding-left': '20px','padding-top': '20px', 'padding-bottom': '20px',
                                                        'margin-top': '10px', 'color': '#003D7C'}),
    html.H2('Comparison of Hours Spent in Central Library between Non-exam and Exam Period',
                style={'font-size': '18px', 'background-color': '#EDF3FF', 
                       'padding': '10px', 'margin': '10px 10px 10px 10px',
                       'border': '1px solid #5F5B5B', 'display': 'inline-block'}),
    html.Div(children=[
        dbc.Row(children=[
            dbc.Col(html.Img(src=dash.get_asset_url('hours_spend_non-exam_bar.png'), style={'width': '50%', 'height': 'auto'})),
            dbc.Col(html.Img(src=dash.get_asset_url('hours_spend_exam_bar.png'), style={'width': '50%', 'height': 'auto'}))
            ]),
        ]),
    *make_break(2),
    
    html.Div(children=[
        dbc.Row([
            dbc.Col([
                html.H2('Seat Choping Analysis',
                    style={'font-size': '18px', 'background-color': '#EDF3FF', 
                        'padding': '10px', 'margin': '10px 10px 10px 10px',
                        'border': '1px solid #5F5B5B', 'display': 'table'}),
                html.Img(src=dash.get_asset_url('seat_choping.png'))
            ]),
            dbc.Col([
                html.H2('Lunch Time Preference',
                    style={'font-size': '18px', 'background-color': '#EDF3FF', 
                        'padding': '10px', 'margin': '10px 10px 10px 10px',
                        'border': '1px solid #5F5B5B', 'display': 'table'}),
                html.Img(src=dash.get_asset_url('lunch_time_preference.png'))
            ]),
            dbc.Col([
                html.H2('Grouping Preference',
                    style={'font-size': '18px', 'background-color': '#EDF3FF', 
                        'padding': '10px', 'margin': '10px 10px 10px 10px',
                        'border': '1px solid #5F5B5B', 'display': 'table'}),
                html.Img(src=dash.get_asset_url('study_reason.png'))
            ]),
        ], style={'marginBottom': '100px'}),
        html.Div(children=[
                html.H5(['69% of library users reserve seats during lunch breaks for an average of ', html.Strong('45'), ' minutes.']),
                html.H5(["Library's ", html.Strong('peak'), " seat occupancy issue occurs between ", html.Strong('11pm to 2pm'), " ."]),
                html.H5(['Around ', html.Strong('12:30pm'), ', 51.7% of these users leave for lunch, worsening the seat hogging problem.'])],
                style={'text-align':'center', 'border':'2px solid black', 'background-color': '#EDF3FF', 
                    'padding': '20px', 'margin': '30px', 'height': '90%'})
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

