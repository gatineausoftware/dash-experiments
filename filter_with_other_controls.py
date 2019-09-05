import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)


df = pd.read_csv(
    'https://raw.githubusercontent.com/'
    'plotly/datasets/master/gapminderDataFiveYear.csv')

countries = set(df['country'])



PAGE_SIZE = 5


app.layout = html.Div([
     dcc.Dropdown(id='countries', options=[
        {'value': x, 'label': x} for x in countries
    ], multi=True, value=['Canada', 'United States']),
    html.Div([
        dash_table.DataTable(
            id='table-filtering',
            columns=[
                {"name": i, "id": i} for i in sorted(df.columns)
            ],
            editable=True,
            filter_action='none',
            sort_action='none',
            sort_mode="multi",
            column_selectable="single",
            page_action='custom',
            page_current=0,
            page_size=10,

        )
        ])
    ])










@app.callback(
    Output('table-filtering', "data"),
    [Input('table-filtering', "page_current"),
     Input('table-filtering', "page_size"),
     Input('countries', 'value')])
def update_table(page_current,page_size, countries_selected):
    if not countries_selected:
        # Return all the rows on initial load/no country selected.
        dff = df
    else:
        dff = df.query('country in @countries_selected')


    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)