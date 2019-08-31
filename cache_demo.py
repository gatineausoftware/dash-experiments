import dash
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)


#imagine this is the full cache of bonds. It is shred between users

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')


#this is an identifier
for i in range(len(df)):
   df.loc[i, 'trade-id'] = str(i)


#add distance column
df['distance']=0

def get_distances(cusip):
    #pretend to call fastscore with cusip + all bonds in cache
    distances = np.random.randint(0, 100, len(df))
    d = {}
    for i in range(len(df)):
        d.update({i: distances[i]})

    #return a map of trade_id: distance
    return d



#corresponding to number closest bonds we want to consider

PAGE_SIZE = 5





app.layout = html.Div([
    html.Label("cusip_label"),
    html.Div(dcc.Input(id='trade-id', type='text')),
    html.Button('fastscore', id='fastscore'),
    dcc.Store(id='distance_cache', storage_type='session'),
    dash_table.DataTable(
    id='table-filtering',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',

    filter_action='custom',
    filter_query=''
    )

     ]
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3



@app.callback(Output('distance_cache', 'data'),
              [Input('fastscore', 'n_clicks')],
              [State('trade-id', 'value')],
              )
def on_click(n_clicks, value):
    # when user clicks button, go find distances from cusip to all bonds in cache
    data = get_distances(value)
    return data


@app.callback(
    Output('table-filtering', "data"),
    [Input('table-filtering', "page_current"),
     Input('table-filtering', "page_size"),
     Input('table-filtering', "filter_query"),
     Input('distance_cache', 'data')])
def update_table(page_current,page_size, filter, distance_cache):
    print(filter)
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]



    for i, row in dff.iterrows():
        cusip = row['trade-id']
        distance = distance_cache[cusip]
        dff.loc[i, 'distance'] = distance

    dff = dff.sort_values('distance')
    dff = dff.iloc[
          page_current * page_size:(page_current + 1) * page_size
          ]

    return dff.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)