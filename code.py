
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import base64
import io

app = Dash(__name__)

data = pd.read_csv('data.csv')

app.layout = html.Div([
    html.Div(children='Погода'),
    html.Hr(),
    dcc.RadioItems(options=[
        {'label': 'давление вечер', 'value': 'давление вечер'},
        {'label': 'облачность день', 'value': 'облачность день'}
    ], value='давление вечер', id='controls-and-radio-item'),
    dash_table.DataTable(data=[], page_size=10, id='data-table'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dcc.Graph(figure={}, id='histogram-chart'),
    dcc.Graph(figure={}, id='line-chart'),
])

@app.callback(
    [Output(component_id='data-table', component_property='data'),
     Output(component_id='controls-and-graph', component_property='figure'),
     Output(component_id='histogram-chart', component_property='figure'),
     Output(component_id='line-chart', component_property='figure')],
    [
     Input(component_id='controls-and-radio-item', component_property='value')
    ]
)
def update_data_and_graph(contents):
    if contents is None:
        contents = 'давление вечер'
    if contents is not None:

        count = len(data['ветер день'])
        for i in range(count):
            d = str(data['ветер день'][i]).split(' ')[0]
            data['ветер день'][i] = d

        fig_hist = px.histogram(data, x=data['id города'], y=data[contents])
        fig_pie = px.pie(data, values=data['id города'], names=data['ветер день'])
        fig_bar = px.bar(data, x=data['давление день'], y=data['id города'])

        return data.to_dict('records'), fig_pie, fig_hist, fig_bar
    else:
        return [], {}, {}, {}


if __name__ == '__main__':
    app.run_server(debug=True)
