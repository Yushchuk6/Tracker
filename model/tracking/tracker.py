from pygeodesy.sphericalNvector import LatLon


class Tracker:
    def __init__(self, error_generator, lat, lon, h):
        self.error_gen = error_generator
        self.latlon = LatLon(lat, lon, h)

    def get_bearing(self, latlon):
        b = self.latlon.initialBearingTo(latlon)
        return b + self.error_gen()

    def get_latlon(self):
        return self.latlon.latlon
