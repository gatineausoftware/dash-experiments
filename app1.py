import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
from flask import Flask, request



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def getcredentials():
    res = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return res.json()["id"]



server = Flask(__name__)


app = dash.Dash(
    __name__,
    server=server,
)

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




app.layout = html.Div([
    dcc.Input(id='user_creds', value=getcredentials(), type='hidden'),
    dcc.Input(id='my-id', type='text'),
    html.Div(id='my-div'),

])



@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='user_creds', component_property='value')]
)

def update_output_div(input_value):
   return str(input_value) + "xxx"


if __name__ == '__main__':
    app.run_server(debug=True)