import numpy as np

from model.move_model.target import Target
from model.tracking.tracker import Tracker
from model.tracking.positioning import Positioning

def err_gen_norm():
    return np.random.normal(0, 1)

class Simulator:
    def __init__(self, path_df, trackers_df, f_error, f_filter):
        self.path = path_df
        self.target = Target(path_df.to_numpy())

        self.tracker_list = list(map(lambda t: Tracker(
            f_error, t[0], t[1], t[2]), trackers_df.to_numpy()
        ))

        self.pos = Positioning(self.tracker_list, f_filter, 5)

    def get_path(self):
        lat = self.path['latitude'].to_list()
        lon = self.path['longitude'].to_list()

        latlon = np.stack((lat, lon), axis=1)

        return latlon.tolist()

    def get_trackers(self):
        latlon = list(map(lambda t: t.get_latlon(), self.tracker_list))
        
        return latlon

    def get_target(self, time):
        latlon = self.target.get_latlon_by_time(time)

        self.pos.add_target_pos(latlon)

        return latlon.latlon

    def get_target_guess(self, time):
        latlon = self.target.get_latlon_by_time(time)

        lat, lon = self.pos.guess_target(latlon).latlon

        return [lat, lon]
