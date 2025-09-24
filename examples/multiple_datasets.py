from graph import SimpleGraph, show
from data import MeasuredData

scatterplot = SimpleGraph("Thoughts vs time thinking")

# first let's set our graph's data and plot the points
hours_thinking = MeasuredData.from_set([0.1, 0.23, 0.29, 0.41, 0.5, 0.52, 0.53], 0.01)
thoughts = MeasuredData.from_set([1, 2, 3, 3.3, 4.9, 5.1, 5.5], 0.05)

scatterplot.set_x_axis(hours_thinking, "Hours thinking (hr)")
scatterplot.set_y_axis(thoughts, "Thoughts (th)")

scatterplot.plot_points()
scatterplot.put_labels()

""" I now have a graph with thoughts vs hours thinking plotted, but I want to graph
along side that data thoughts squared and thoughts cubed. Luckily, I can do so by just
setting my graph to a different set of data and calling plot_points() again, which
will draw the new dataset alongside the old one!"""

thoughts_squared = [thought ** 2 for thought in thoughts]
thoughts_cubed   = [thought ** 3 for thought in thoughts]

scatterplot.set_y_axis(thoughts_squared, "Thoughts squared (th^2")
# since my x-axis is staying the same, I don't need to change it. I could though, if needed be.
scatterplot.plot_points()

scatterplot.set_y_axis(thoughts_cubed, "Thoughts cubed (th^3)")
scatterplot.plot_points()

# So that people can tell which sets of data are which,
# I can use .put_legend() to add a legend to my graph
scatterplot.put_legend()

# make a window with our graph
show()