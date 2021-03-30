from move_model.target import Target
from tracking.tracker import Tracker
import numpy as np
import plotly.express as px
import pandas as pd
import time
import csv


def main():
  df = pd.read_csv('test2.csv')
  target = Target(df.to_numpy())

  # fig = px.line_3d(df, x="x", y="y", z="z")
  # fig.show()
  for p in range(10000):
    coords = target.get_coords(p*0.1)
    print(coords)

  
  # for p in range(10000):
  #     figure.canvas.draw()

  #     coords = t.get_coords(p*0.1)

  #     if dot1 != None:
  #       ax.collections.remove(dot1)
  #     dot1 = ax.scatter(*coords,s=50, c='green')

  #     figure.canvas.flush_events()
  #     time.sleep(0.01)

  # slider = Slider(ax, 'Time', 0.0, 30.0, valinit=0)
  # slider.on_changed(update)
  # def update(val):
  #     time = slider.val
  #     coords = t.get_coords(p*time)
  #     dot1.set_xdata(coords[0])
  #     dot1.set_ydata(coords[1])
  #     dot1.set_zdata(coords[2])
  #     figure.canvas.draw_idle()
  


main()