import numpy as np
from pygeodesy.sphericalNvector import LatLon


class Tracker:
    def __init__(self, error_generator, lat, lon, h):
        self.error_gen = error_generator
        self.latlon = LatLon(lat, lon, h)

    def get_bearing(self, latlon):
        b = self.latlon.initialBearingTo(latlon)
        return b + self.error_gen()

    # def get_angle(self, x, y, z):
    #   return calc_angle_3d([x,y,z]-self.coords,
    #                       self.vector_north)

    # def get_z_angle(self, x, y, z):
    #   return calc_angle_2d(([y,self.coords[2]]),
    #                       ([y,z]))
