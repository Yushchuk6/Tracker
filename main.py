from move_model.target import Target
from tracking.tracker import Tracker
from tracking.positioning import Positioning
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
from pygeodesy.sphericalNvector import LatLon
from pygeodesy.sphericalNvector import triangulate


def main():
    table = pd.read_csv("test3.csv")
    target = Target(table.to_numpy())
    # tr = []
    # for segment in t.directions:
    #   print(segment.latlon)
    #   tr.append(segment.latlon)

    # tr = np.array(tr).transpose()
    # x = tr[0]
    # y = tr[1]
    # z = tr[2]

    plt.ion()

    figure = plt.figure()
    ax = figure.add_subplot(111, projection='3d')

    ax.view_init(elev=90, azim=-90)

    dot1 = None
    line1 = ax.plot(table['longitude'], table['latitude'],
                    table['height'], label='trajectory')

    for p in range(10000):
        figure.canvas.draw()

        coords = target.get_latlon_by_time(p*0.5)
        [y, x, z] = coords.latlonheight

        if dot1 != None:
            ax.collections.remove(dot1)
        dot1 = ax.scatter(x, y, z, s=50, c='green')

        figure.canvas.flush_events()
        time.sleep(0.01)


# def read_csv(path):
#   with open(path) as file:
#     data = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
#     return data

def err_gen_norm():
    return np.random.normal(0, 1)


def err_none():
    return 0


def test():
    # p = LatLon("47°18.228'N","002°34.326'W")  # Basse Castouillet
    # q = LatLon("47°18.664'N","002°31.717'W")  # Basse Hergo
    # t = triangulate(p, 7, q, 295)  # 47.323667°N, 002.568501°W'
    # print(t)
    tracker1 = Tracker(err_none, 1, 5, 5)
    tracker2 = Tracker(err_none, 2, 1.8, 2)

    target = LatLon(2, 2, 40)

    a1 = tracker1.get_bearing(target)
    a2 = tracker2.get_bearing(target)
    print(a1, a2)
    print(target)

    p = Positioning()
    print(p.triangulate(tracker1.latlon, a1,
                        tracker2.latlon, a2))

    # pos = Positioning(north)
    # pos.calc_coord(trac_v,a1, trac_v2, a2)


test()
