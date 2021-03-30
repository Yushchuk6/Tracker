import numpy as np

class Positioning:
  def __init__(self, north):
    self.vector_north = north

  def calc_coord(self, c1, a1, c2, a2):
    u = c2[0] - c1[0] 
    v = c2[1] - c1[1]
    a3 = np.pi - (a1 + a2)
    A = np.array([[u, v], [-v, u]])
    B = np.array([a2*a3*np.cos(a1)+u*c1[0] + v*c1[1],
                  a2*a3*np.sin(a1)+u*c2[1] - v*c2[0]])
    res = np.linalg.solve(A, B)
    print(res)
  
  def triangle_angle(self, c1, c2, a):
    line = c2-c1
    