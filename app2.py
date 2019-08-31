import dash
import dash_html_components as html
import dash_core_components as dcc
from flask import Flask, request


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



server = Flask(__name__)
server.config['supports_credentials'] = True

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/'
)

app.layout = html.Div([
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    print(request.headers)
    return request.headers['Host']



if __name__ == '__main__':
    app.run_server(debug=True)