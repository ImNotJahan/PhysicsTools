from physics_tools.graph import SimpleGraph, show
from physics_tools.data import MeasuredData

scatterplot = SimpleGraph("Thoughts vs hours thinking")

# first let's set our graph's data and plot the points
x_axis_data = MeasuredData.from_set([0.1, 0.23, 0.29, 0.41, 0.5, 0.52, 0.53], 0.03)
y_axis_data = MeasuredData.from_set([1, 2, 3, 3.3, 4.9, 5.1, 5.5], 0.01)

scatterplot.set_x_axis(x_axis_data, "Hours thinking (hr)")
scatterplot.set_y_axis(y_axis_data, "Thoughts (th)")

scatterplot.plot_points() # if I didn't want the actual points to be on the graph, I could comment this out

# put the x- and y-axis labels on our graph
scatterplot.put_labels()

""" WOAH BIG IMPORTANT METHOD WHICH IS THE POINT OF THIS EXAMPLE!!!!
calling the best_fit method on my graph will draw a line of best fit
information about the line is returned as a tuple """
line_info = scatterplot.best_fit()

# this will tell us ((slope, uncertainty), (y-intercept, uncertainty))
print(line_info)

# make a window with our graph
show()