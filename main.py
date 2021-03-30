import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import numpy as np


from move_model.target import Target
from tracking.tracker import Tracker
from tracking.positioning import Positioning

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def err_gen_norm():
    return np.random.normal(0, 1)


def calc_center(lat_list, lon_list):
    lat = np.mean(lat_list)
    lon = np.mean(lon_list)
    return lat, lon


def create_figure(df, pos):
    fig = go.Figure(
        data=[go.Scattermapbox(mode="markers+lines",
                               lat=df['latitude'],
                               lon=df['longitude'],
                               marker=dict(color="blue", size=15),
                               name="path"),
              go.Scattermapbox(mode="markers",
                               lat=[50.45],
                               lon=[30.45],
                               marker=dict(color="green", size=15),
                               name="target"),
              go.Scattermapbox(mode="markers",
                               lat=[50.45],
                               lon=[30.45],
                               marker=dict(color="purple", size=15),
                               name="guess_target"),
              go.Scattermapbox(mode="markers+lines",
                               lat=pos.get_lat_list(),
                               lon=pos.get_lon_list(),
                               marker=dict(color="red", size=15),
                               name="trakers")],
        layout=go.Layout(
            uirevision='true')
    )

    lat, lon = calc_center(df['latitude'], df['longitude'])

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lat': lat, 'lon': lon},
            'style': "white-bg",  # open-street-map
            'zoom': 14.5})

    return fig


def create_layout(fig, target, pos):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Div([
            dcc.Graph(id="graph", figure=fig,
                      style={'width': '80%', 'height': '90vh'}),
            html.Div([
                html.Div(children="hello 1"),
                html.Div([
                    dcc.Input(id="input1", type="text", placeholder="1"),
                    dcc.Input(id="input2", type="text", placeholder="2"),
                ], style={'display': 'flex', 'align-self': 'flex-start'}),
                html.Div(children="hello 2"),
                html.Div([
                    dcc.Input(id="input4", type="text", placeholder="1"),
                    dcc.Input(id="input5", type="text", placeholder="2"),
                ]),
            ], style={'flex-direction': 'column'})
        ], style={'display': 'flex'}),
        html.Button('Play', id='play', n_clicks=0),
        dcc.Slider(
            id='my-slider',
            min=0,
            max=target.total_time,
            step=0.1,
            value=0,
        ),
        dcc.Interval(
            id='interval-component',
            interval=100,
            n_intervals=0,
            disabled=True
        ),
    ])

    @ app.callback(
        Output("graph", "figure"),
        Input('my-slider', 'value'),
        State("graph", "figure"))
    def resize_figure(time, fig_json):
        fig = go.Figure(fig_json)

        latlon = target.get_latlon_by_time(time)
        [lat, lon, h] = latlon.latlonheight

        trace = [trace for trace in fig.data if trace.name == "target"][0]
        trace.update(lat=[lat], lon=[lon])
        [lat, lon, h] = pos.guess_target(latlon).latlonheight

        trace = [trace for trace in fig.data if trace.name == "guess_target"][0]
        trace.update(lat=[lat], lon=[lon])

        return fig

    @ app.callback(
        Output('interval-component', 'disabled'),
        Input('play', 'n_clicks'),
        State('interval-component', 'disabled'),
        prevent_initial_call=True)
    def update_output(n, status):
        return not status

    @ app.callback(
        Output('my-slider', 'value'),
        Input('interval-component', 'n_intervals'),
        State('my-slider', 'value'),
        State('my-slider', 'step'),
        State('my-slider', 'max'))
    def update_metrics(n, value, step, max):
        if value >= max:
            return 0
        return value + step*3

    return app


if __name__ == '__main__':
    df = pd.read_csv('test3.csv')

    target = Target(df.to_numpy())

    tracker_list = []
    # test_medium
    tracker_list.append(Tracker(err_gen_norm, 50.465, 30.46, 5))
    tracker_list.append(Tracker(err_gen_norm, 50.445, 30.43, 20))
    tracker_list.append(Tracker(err_gen_norm, 50.438, 30.48, 20))
    # test_large
    # tracker_list.append(Tracker(err_gen_norm, 50.48, 30.45, 5))
    # tracker_list.append(Tracker(err_gen_norm, 50.43, 30.38, 20))
    # tracker_list.append(Tracker(err_gen_norm, 50.42, 30.5, 20))
    # test_small
    # tracker_list.append(Tracker(err_gen_norm, 50.448, 30.448, 5))
    # tracker_list.append(Tracker(err_gen_norm, 50.452, 30.458, 20))
    # tracker_list.append(Tracker(err_gen_norm, 50.446, 30.46, 20))

    p = Positioning(tracker_list)

    fig = create_figure(df, p)
    app = create_layout(fig, target, p)

    app.run_server(debug=True)
