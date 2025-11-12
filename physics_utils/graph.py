import numpy as np
import matplotlib.pyplot as plt
from .data import MeasuredData

def show():
    """
    Displays all created graphs
    """
    plt.show()

class SimpleGraph:
    """
    Creates a plot with automatic error bars
    """
    def __init__(self, title: str):
        fig, ax = plt.subplots()
        self.figure = fig
        self.axes = ax
        self.title = title

        # initialize some things as empty
        self.x_data = []
        self.x_error = []
        self.x_label = ""
        self.y_data = []
        self.y_error = []
        self.y_label = ""

    def set_x_axis(self, values: list[MeasuredData], label: str) -> None:
        """
        Sets the x-axis values and error

        Parameters
        ----------
        values : list[MeasuredData]
            The data points for the x-axis
        label : str
            The label for these data points

        Examples
        --------
        >>> graph = SimpleGraph("New Graph")
        >>> graph.set_x_axis([MeasuredData(0, 1), MeasuredData(1, 1), MeasuredData(2, 1)], "X-Axis")
        >>> graph.x_data
        [0.0, 1.0, 2.0]
        >>> graph.x_error
        [1, 1, 1]
        >>> graph.x_label == "X-Axis"
        True
        """
        self.x_label = label
        self.x_data = [float(x) for x in values]
        self.x_error = [x.error() for x in values]

    def set_y_axis(self, values: list[MeasuredData], label: str) -> None:
        """
        Sets the y-axis values and error

        Parameters
        ----------
        values : list[MeasuredData]
            The data points for the y-axis
        label : str
            The label for these data points
        """
        self.y_label = label
        self.y_data = [float(x) for x in values]
        self.y_error = [x.error() for x in values]

    def plot_points(self) -> None:
        """
        Plots the currently set x- and y-axes on the graph, with error bars
        """
        #self.axes.plot(self.x_data, self.y_data, ".")
        self.axes.errorbar(
            self.x_data, self.y_data,
            yerr=self.y_error, xerr=self.x_error,
            fmt=".", capsize=2, label=self.y_label
        )

    def best_fit(self, return_as_md=False) -> tuple:
        """
        Creates a linear line of best fit on the graph, for the last set x- and y-axes

        Returns
        -------
        tuple
            Returns a tuple containing two tuples, with both tuples containing two values - the first value being
            a measurement, and the second an uncertainty.
            The first tuple represents the slope; and the second, the y-intercept.
        """
        linearfit, covariance_matrix = np.polyfit(self.x_data, self.y_data, 1, cov=True)
        fitted_y = [linearfit[1] + i * linearfit[0] for i in self.x_data]
        self.axes.plot(self.x_data, fitted_y, label="Line of Best Fit")

        if return_as_md:
            return (
                MeasuredData(float(linearfit[0]), float(np.sqrt(covariance_matrix[0][0]))),
                MeasuredData(float(linearfit[1]), float(np.sqrt(covariance_matrix[1][1])))
            )
        else:
            return (
                (linearfit[0], np.sqrt(covariance_matrix[0][0])),
                (linearfit[1], np.sqrt(covariance_matrix[1][1]))
            )

    def put_labels(self) -> None:
        """
        Adds axes labels to the graph, using the labels given on the last sets of x- and y-axes datas
        """
        self.axes.set(title=self.title, xlabel=self.x_label, ylabel=self.y_label)

    def put_legend(self) -> None:
        """
        Adds a legend to the graph
        """
        self.axes.legend()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
