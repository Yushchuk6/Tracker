from .segment import Segment
from dataclasses import dataclass
from pygeodesy.sphericalNvector import LatLon


class Target:
    def __init__(self, matrix):
        self.directions = [Segment(None, *matrix[0])]
        self.total_time = 0

        for i in range(1, len(matrix)):
            predecessor = self.directions[i-1]
            self.directions.append(Segment(predecessor, *matrix[i]))
            self.total_time += self.directions[i].total_time

    def get_latlon_by_time(self, time):
        t = 0
        d = self.directions
        for i in range(1, len(d)):
            if (d[i].total_time + t) <= time:
                t += d[i].total_time
            else:
                return d[i].get_latlon_by_time(time - t)
        return LatLon(0, 0, 0)
