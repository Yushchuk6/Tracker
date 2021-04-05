import numpy as np
from pygeodesy.sphericalNvector import triangulate, LatLon


class Positioning:
    def __init__(self, tracker_list, filter):
        self.tracker_list = tracker_list
        if len(tracker_list) > 2:
            self.tracker_list.append(tracker_list[0])
        
        self.filter = filter
        self.lat_list = []
        self.lon_list = []

    def get_lat_list(self):
        return list(map(lambda x: x.latlon.lat, self.tracker_list))

    def get_lon_list(self):
        return list(map(lambda x: x.latlon.lon, self.tracker_list))

    def triangulate(self, ll1, b1, ll2, b2):
        main_ll, main_b, sub_ll, sub_b = self._sort_main_sub(ll1, b1, ll2, b2)

        bearing = main_ll.initialBearingTo(sub_ll)

        if (main_b - bearing) >= 0 and (main_b - bearing) < 180:
            return triangulate(sub_ll, sub_b, main_ll, main_b)
        else:
            return triangulate(main_ll, main_b, sub_ll, sub_b)

    def _sort_main_sub(self, ll1, b1, ll2, b2):
        if ll1.lon - ll2.lon >= 0:
            return ll2, b2, ll1, b1
        else:
            return ll1, b1, ll2, b2

    def guess_target(self, target):
        size = len(self.tracker_list) - 1
        lat, lon = 0, 0

        for i in range(0, size):
            guess = self.guess_position(
                self.tracker_list[i],
                self.tracker_list[i+1],
                target)
            lat += guess.lat
            lon += guess.lon

        lat /= size
        lon /= size

        self.lat_list.append(lat)
        self.lon_list.append(lon)

        lat, lon = self.filter(self.lat_list, self.lon_list)
        return LatLon(lat, lon)

    def guess_position(self, tracker1, tracker2, target):
        a1 = tracker1.get_bearing(target)
        a2 = tracker2.get_bearing(target)

        return self.triangulate(tracker1.latlon, a1,
                                tracker2.latlon, a2)
