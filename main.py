import numpy as np
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from pykalman import KalmanFilter


from move_model.target import Target
from tracking.tracker import Tracker
from tracking.positioning import Positioning


def err_gen_norm():
    return np.random.normal(0, 1)


def ewm(_list):
    df = pd.DataFrame(_list)

    avg = df.ewm(span=len(_list), adjust=False).mean()

    return avg.values.tolist()[-1][0]

def kalman(_list):
    kf = KalmanFilter(initial_state_mean=_list[0])

    res, _ = kf.em(_list, n_iter=2).smooth(_list)

    return res[-1][0]


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
                      style={'width': '100%', 'height': '90vh'}),
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
            interval=1000,
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
        State('interval-component', 'interval'),
        State('my-slider', 'value'),
        State('my-slider', 'step'),
        State('my-slider', 'max'))
    def update_metrics(n, interval, value, step, max):
        if value >= max:
            return 0
        return value + interval/1000

    return app


if __name__ == '__main__':
    path_df = pd.read_csv('path.csv')
    target = Target(path_df.to_numpy())

    trackers_df = pd.read_csv('trackers_medium.csv')
    tracker_list = list(map(lambda t: Tracker(
        err_gen_norm, t[0], t[1], t[2]), trackers_df.to_numpy()))

    p = Positioning(tracker_list, ewm, 5)

    fig = create_figure(path_df, p)
    app = create_layout(fig, target, p)

    app.run_server(debug=True)
