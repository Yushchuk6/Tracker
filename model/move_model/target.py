from .segment import Segment
from dataclasses import dataclass
from pygeodesy.sphericalNvector import LatLon


class Target:
    def __init__(self, matrix):
        self.segments = [Segment(None, *matrix[0])]
        self.total_time = 0

        for i in range(1, len(matrix)):
            predecessor = self.segments[i-1]
            self.segments.append(Segment(predecessor, *matrix[i]))
            self.total_time += self.segments[i].total_time

    def get_latlon_by_time(self, time):
        t = 0
        s = self.segments
        for i in range(1, len(s)):
            if (s[i].total_time + t) <= time:
                t += s[i].total_time
            else:
                return s[i].get_latlon_by_time(time - t)
        return LatLon(0, 0, 0)

    def get_total_time(self):
        time = 0
        for s in self.segments:
            time += s.total_time
        return time
