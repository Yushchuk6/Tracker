import numpy as np
import math
from pygeodesy.sphericalNvector import Nvector, LatLon


class Segment:
    def __init__(self, predecessor, lat, lon, h, a, v0=0):
        if predecessor == None:
            self.start_latlon = LatLon(0, 0, 0)
            self.v0 = v0
        else:
            self.start_latlon = predecessor.latlon
            self.v0 = predecessor.v

        self.latlon = LatLon(lat, lon, h)
        self.total_time = self.get_time(a, self.v0,
                                        self.start_latlon.distanceTo(self.latlon))
        self.a = a
        self.v = self.get_speed(self.total_time)

    def get_latlon_by_time(self, time):
        distance = self.v0 * time + self.a * pow(time, 2) / 2
        bearing = self.start_latlon.initialBearingTo(self.latlon)
        return self.start_latlon.destination(distance, bearing, height=self.start_latlon.height)

    def get_time(self, a, v0, s):
        if a == 0:
            return 0 if v0 == 0 else s/v0
        else:
            d = pow(v0, 2) + (2*a*s)
            return abs((-v0+math.sqrt(abs(d)))/a)

    def get_speed(self, time):
        return self.v0 + self.a * time
