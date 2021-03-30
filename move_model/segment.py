import numpy as np
import math


class Segment:
  def __init__(self, predecessor, x, y, z, a ,v0 = 0):
    if predecessor == None:
      self.start_coords = np.array([0,0,0])
      self.v0 = v0
    else:
      self.start_coords = predecessor.coords
      self.v0 = predecessor.v
    
    self.coords = np.array([x,y,z])
    vector = self.coords-self.start_coords
    length = np.linalg.norm(vector)
    self.unit_vector = vector/length
    self.total_time = self.get_time(a, self.v0, length) 
    self.a = a
    self.v = self.get_speed(self.total_time)
  
  def get_coords(self, time):
    distance = self.v0 * time + self.a * pow(time, 2) / 2
    return self.start_coords + self.unit_vector * distance
  
  def get_time(self, a ,v0 ,s):
    if a == 0:
      return 0 if v0 == 0 else s/v0
    else:
      d = pow(v0, 2) + (2*a*s)
      return abs((-v0+math.sqrt(abs(d)))/a)

  def get_speed(self, time):
    return self.v0 + self.a * time
