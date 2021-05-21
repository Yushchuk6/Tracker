import json
import asyncio
import pandas as pd
import numpy as np
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


class SimTragetController:
    time = 1

    def __init__(self, path_df, trackers_df, f_error, f_filter):
        self.path = path_df
        self.target = Target(path_df.to_numpy())

        self.tracker_list = list(map(lambda t: Tracker(
            f_error, t[0], t[1], t[2]), trackers_df.to_numpy()))

        self.pos = Positioning(self.tracker_list, f_filter, 5)

    def get_path_json(self):
        data = {
            'name': 'path',
            'lat': self.path['latitude'].to_list(),
            'lon': self.path['longitude'].to_list(),
        }

        res = {
            'type': 'trace',
            'data': data,
        }

        return json.dumps(res)

    def get_path_center_json(self):
        lat = self.path['latitude'].to_list()
        lon = self.path['longitude'].to_list()

        data = {
            'mapbox': {
                'center': {'lat': np.mean(lat), 'lon': np.mean(lon)},
                'style': 'open-street-map',
                'zoom': 14.5,
            }
        }

        res = {
            'type': 'layout',
            'data': data,
        }

        return json.dumps(res)

    def get_target(self):
        lat, lon = self.target.get_latlon_by_time(self.time).latlon
        
        data = {
            'name': 'target',
            'lat': [lat],
            'lon': [lon],
        }

        res = {
            'type': 'trace',
            'data': data,
        }

        return json.dumps(res)
    
    def get_target_guess(self):
        latlon = self.target.get_latlon_by_time(self.time)

        lat, lon = self.pos.guess_target(latlon).latlon

        data = {
            'name': 'target_guess',
            'lat': [lat],
            'lon': [lon],
        }

        res = {
            'type': 'trace',
            'data': data,
        }

        return json.dumps(res)

