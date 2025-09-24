from graph import SimpleGraph, show
from data import MeasuredData

scatterplot = SimpleGraph("My graph")

# All of my x-axis measurements have the same reading error, so I'll turn them
# all into MeasuredData objects at the same time by using the MeasuredData.from_set method
x_axis_data = MeasuredData.from_set([1.0, 1.8, 2.1, 2.7, 3.5], 0.05)
# x_axis_data == list of MeasuredData's

# My y-axis measurements have varying standard error, so I typed
# them all out explicitly in a list here
y_axis_data = [
    MeasuredData(5.01, 0, 0.1),
    MeasuredData(5.5, 0, 0.2),
    MeasuredData(7, 0, 0.1),
    MeasuredData(2, 0, 0.07),
    MeasuredData(8, 0, 1.5)
]

# set the data and give each axis a label
scatterplot.set_x_axis(x_axis_data, "Height (m)")
scatterplot.set_y_axis(y_axis_data, "Vorps (?)")

# plot the points we set with set_x_axis and set_y_axis,
# along with their error shown as bars
scatterplot.plot_points()

# put the x- and y-axis labels on our graph
scatterplot.put_labels()

# make a window with our graph
show()