from .segment import Segment
from dataclasses import dataclass

class Target:
  def __init__(self, matrix):
    self.directions = [Segment(None, *matrix[0])]
    for i in range(1, len(matrix)):
      predecessor = self.directions[i-1]
      self.directions.append(Segment(predecessor, *matrix[i]))
  
  def get_coords(self, time):
    t = 0
    d = self.directions
    for i in range(1, len(d)):
      if (d[i].total_time + t) <= time:
        t +=d[i].total_time
      else:
        return d[i].get_coords(time - t)
    return [0,0,0]
