import numpy as np
import math
from pygeodesy.sphericalNvector import Nvector, LatLon


class Segment:
    def __init__(self, predecessor, lat, lon, h, a, v0=0):
        if predecessor is None:
            self.start_latlon = LatLon(0, 0, 0)
            self.v0 = v0
        else:
            self.start_latlon = predecessor.latlon
            self.v0 = predecessor.v

        self.latlon = LatLon(lat, lon, h)
        self.a = a
        self.total_time = self.get_time(self.start_latlon.distanceTo(self.latlon))
        self.v = self.get_speed(self.total_time)

    def get_latlon_by_time(self, time):
        if time <= 0:
            time = 0.00000001
        distance = self.v0 * time + self.a * pow(time, 2) / 2
        bearing = self.start_latlon.initialBearingTo(self.latlon)
        return self.start_latlon.destination(distance, bearing, height=self.start_latlon.height)

    def get_time(self, s):
        if self.a == 0:
            return 0 if self.v0 == 0 else s/self.v0
        else:
            d = pow(self.v0, 2) + (2*self.a*s)
            return abs((-self.v0+math.sqrt(abs(d)))/self.a)

    def get_speed(self, time):
        return self.v0 + self.a * time
