from pygeodesy.sphericalNvector import triangulate, LatLon


class Positioning:
    def __init__(self, tracker_list, filter, accuracy):
        self.tracker_list = tracker_list
        if len(tracker_list) > 2:
            self.tracker_list.append(tracker_list[0])

        self.filter = filter
        self.accuracy = accuracy
        self.guess_lat_list = []
        self.guess_lon_list = []

    def get_tracker_lat_list(self):
        return list(map(lambda x: x.latlon.lat, self.tracker_list))

    def get_tracker_lon_list(self):
        return list(map(lambda x: x.latlon.lon, self.tracker_list))

    def guess_target(self, target):
        self._add_target_pos(target)

        lat = self.filter(self.guess_lat_list)
        lon = self.filter(self.guess_lon_list)

        return LatLon(lat, lon)

    def _add_target_pos(self, target):
        size = len(self.tracker_list) - 1
        lat, lon = 0, 0

        for i in range(0, size):
            guess = self._guess_position(
                self.tracker_list[i],
                self.tracker_list[i+1],
                target)
            lat += guess.lat
            lon += guess.lon

        lat /= size
        lon /= size

        self.guess_lat_list.append(lat)
        self.guess_lon_list.append(lon)

        self._update_list(self.guess_lat_list)
        self._update_list(self.guess_lon_list)

    def _update_list(self, _list):
        while len(_list) > self.accuracy:
            del _list[0]

    def _guess_position(self, tracker1, tracker2, target):
        a1 = tracker1.get_bearing(target)
        a2 = tracker2.get_bearing(target)

        return self.triangulate(tracker1.latlon, a1,
                                tracker2.latlon, a2)

    def triangulate(self, ll1, b1, ll2, b2):
        main_ll, main_b, sub_ll, sub_b = self._sort_main_sub(ll1, b1, ll2, b2)

        bearing = main_ll.initialBearingTo(sub_ll)

        if 0 <= (main_b - bearing) < 180:
            return triangulate(sub_ll, sub_b, main_ll, main_b)
        else:
            return triangulate(main_ll, main_b, sub_ll, sub_b)

    def _sort_main_sub(self, ll1, b1, ll2, b2):
        if ll1.lon - ll2.lon >= 0:
            return ll2, b2, ll1, b1
        else:
            return ll1, b1, ll2, b2
