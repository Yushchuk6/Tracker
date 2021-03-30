import numpy as np
from numpy.linalg import norm

def calc_angle_3d(c1, c2):
    return np.arccos(np.dot(c1, c2)/(norm(c1)*norm(c2)))

def calc_angle_2d(c1, c2):
    angle = np.arctan2(np.cross(c1, c2), np.dot(c1, c2))
    if angle < 0:
        angle += 2*np.pi 
    return angle

# def unit_vector(vector):
#     return vector / norm(vector)