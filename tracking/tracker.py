import numpy as np
from mathfunc.angles import calc_angle_3d, calc_angle_2d

class Tracker:
  def __init__(self, error_generator, north, x, y, z):
    self.error_gen = error_generator
    self.vector_north = north
    self.coords = np.array([x,y,z])

  def get_angle(self, x, y, z):
    return calc_angle_3d([x,y,z]-self.coords,
                        self.vector_north)

  def get_xy_angle(self, x, y, z=0):
    return calc_angle_2d(([x,y,z]-self.coords)[:2],
                        self.vector_north[:2])   
  
  def get_z_angle(self, x, y, z):
    return calc_angle_2d(([y,self.coords[2]]),
                        ([y,z]))