"""
Defines the MeasuredData class and helper functions for error propagation
"""

__all__ = ["MeasuredData", "avg_from_set", "avg_measured_datas"]

import math
import numpy as np
import pandas as pd
from typing import Iterable, Self

safe_div = lambda x, y: 0 if y == 0 else x / y

class MeasuredData:
    """
    Represents a numerical measurement with uncertainty

    Attributes
    ----------
    value : float
        The actual value of the data
    reading_error : float
        The error from the instrument reading
    standard_error : float
        The statistical standard error

    Notes
    -----
    This class automatically propagates uncertainty through calculations
    """
    def __init__(self, measurement: float, reading_error: float, standard_error=0.0):
        self.value = measurement
        self.reading_error = reading_error
        self.standard_error = standard_error

    def error(self) -> float:
        """
        Returns the uncertainty on the data, which is taken to be the greatest error it has

        Examples
        --------
        >>> MeasuredData(100.2, 2.4, 10.12).error()
        10.12
        """
        return max(abs(self.reading_error), abs(self.standard_error))

    def __int__(self) -> int:
        """
        Returns the value of this point truncated to an integer

        Examples
        --------
        >>> int(MeasuredData(100.2, 2, 10))
        100
        """
        return int(self.value)

    def __float__(self) -> float:
        """
        Returns the value of this point as a float

        Examples
        --------
        >>> float(MeasuredData(100.2, 2, 10))
        100.2
        """
        # we still wrap it in a float conversion
        # just incase the provided value for the
        # data point was an int or something
        return float(self.value)

    def __add__(self, other) -> Self:
        """
        Support for addition with a MeasuredData as the left operand

        Examples
        --------
        >>> print(MeasuredData(10.4, 0.0, 0.5) + MeasuredData(3.0, 1.0, 0.2))
        13.0±1.
        >>> print(MeasuredData(12.34, 0.05, 0.02) + 10.111)
        22.45±0.05
        """
        if isinstance(other, MeasuredData):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return MeasuredData(
                self.value + other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        return MeasuredData(self.value + other, self.reading_error, self.standard_error)

    def __radd__(self, other) -> Self:
        """
        Support for addition with a MeasuredData as the right operand
        """
        # addition is symmetric
        return self.__add__(other)

    def __sub__(self, other) -> Self:
        """
        Support for subtraction with a MeasuredData as the left operand
        """
        if isinstance(other, MeasuredData):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return MeasuredData(
                self.value - other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        return MeasuredData(self.value - other, self.reading_error, self.standard_error)

    def __mul__(self, other) -> Self:
        """
        Support for multiplication with a MeasuredData as the left operand
        """
        if isinstance(other, MeasuredData):
            def error(sx, sy) -> float:
                return (
                            (self.value * other.value) *
                            math.sqrt (
                                safe_div(sx, self.value) ** 2 +
                                safe_div(sy, other.value) ** 2
                            )
                        )

            return MeasuredData(
                self.value * other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: (self.value * other) * safe_div(s, self.value)

        return MeasuredData(self.value * other, error(self.reading_error), error(self.standard_error))

    def __rmul__(self, other) -> Self:
        """
        Support for multiplication with a MeasuredData as the right operand
        """
        # multiplication is symmetric
        return self.__mul__(other)

    def __truediv__(self, other) -> Self:
        if isinstance(other, MeasuredData):
            def error(sx, sy) -> float:
                return (
                            (self.value / other.value) *
                            math.sqrt (
                                (sx / self.value) ** 2 +
                                (sy / other.value) ** 2
                            )
                        )

            return MeasuredData(
                self.value / other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: (self.value / other) * safe_div(s, self.value)

        return MeasuredData(self.value / other, error(self.reading_error), error(self.standard_error))

    def __pow__(self, other: int) -> Self:
        """
        Support for taking a MeasuredData to some integer power
        """
        error = lambda s: abs(other * self.value ** (other - 1) * s)

        return MeasuredData(
            self.value ** other,
            error(self.reading_error),
            error(self.standard_error)
        )

    def sine(self) -> Self:
        """
        Takes the result of sin(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: abs(s * math.cos(self.value))

        return MeasuredData(
            math.sin(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def cosine(self) -> Self:
        """
        Takes the result of cos(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: abs(s * math.sin(self.value))

        return MeasuredData(
            math.cos(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def tangent(self) -> Self:
        """
        Takes the result of tan(x) on a MeasuredData with the MeasuredData treated as radians
        """
        return self.sine() / self.cosine()

    def arctan(self) -> Self:
        """
        Takes the result of arctan(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: s / (1 + self.value ** 2)

        return MeasuredData(
            math.atan(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def arcsin(self) -> Self:
        """
        Takes the result of arcsin(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: s / math.sqrt(1 - self.value ** 2)

        return MeasuredData(
            math.asin(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def __neg__(self) -> Self:
        """
        Creates a new MeasuredData with the value negated
        """
        return self.__mul__(-1)

    def __abs__(self) -> Self:
        """
        Creates a new MeasuredData having the absolute value of the old value
        """
        return MeasuredData(
            abs(self.value),
            self.reading_error,
            self.standard_error
        )



    def __str__(self) -> str:
        """
        Converts this MeasuredData into a string representation, showing the value and uncertainty
        The uncertainty is rounded to one digit, and the value is then rounded to the same place as the uncertainty

        Examples
        --------
        >>> str(MeasuredData(1234.56789, 0.05333))
        '1234.57±0.05'
        >>> str(MeasuredData(100.4, 0.0, 4.3))
        '100.0±4.'
        >>> str(MeasuredData(1234.567, 543, 0))
        '1200.0±500.'
        """
        err = np.format_float_positional(self.error(), precision=1, fractional=False)

        decimal_num = 0
        change = -1
        for c in err[1:-1]:
            decimal_num += change
            if c == '.':
                change = 1
                decimal_num = 0

        if err[-1] != '.':
            decimal_num += change

        return str(round(self.value, decimal_num)) + "±" + err

    def latex(self) -> str:
        """
        Converts the MeasuredData into a string representation, as described in the __str__ method, but uses the LaTeX
        symbol for ±, and wraps the value in $$
        """
        parts = str(self).split("±")

        return "${} \\pm {}$".format(parts[0], parts[1])

    @staticmethod
    def from_set(measurements: Iterable[float], reading_error: float, standard_error=0.0) -> list[Self]:
        """
        Takes a bunch of measurements that all have the same error, and converts them all into MeasuredDatas

        Parameters
        ----------
        measurements : Iterable[float]
            An iterable full of values to be converted to MeasuredDatas
        reading_error : float
            The reading error that all the measurements share
        standard_error : float
            The standard error that all the measurements share

        Returns
        -------
        list[Self]
            A list full of MeasuredDatas, with each one corresponding to an element from the measurements parameter,
            and the reading_error and standard_error attributes matching that which were passed as parameters
        """
        return [MeasuredData(x, reading_error, standard_error) for x in measurements]

# from here on out we have some utility functions
def csv_to_numpy(file_name: str, rotate=False) -> np.ndarray:
    if rotate:
        return pd.read_csv(file_name).T.to_numpy()
    return pd.read_csv(file_name).to_numpy()


def remove_nan(data_points: np.ndarray) -> list:
    return [x for x in data_points if not np.isnan(x)]


def remove_nan_2d(data_points: np.ndarray) -> list:
    return [remove_nan(x) for x in data_points]

def avg_from_set(measurements: list[float], reading_error: float) -> MeasuredData:
    """
    Averages a list of floats all having the same error

    Parameters
    ----------
    measurements : list[float]
        The measurements to be averaged
    reading_error : float
        The error which all of the measurements share

    Returns
    -------
    MeasuredData
        The average of all the measurements, with the uncertainty propagated
    """
    n = len(measurements)
    average = sum(measurements) / n
    standard_deviation = math.sqrt(
        (1 / (n - 1)) * sum(([(x - average)**2 for x in measurements]))
    )
    return MeasuredData(average, reading_error, standard_deviation / math.sqrt(n))

def avg_measured_datas(measurements: list[MeasuredData]) -> MeasuredData:
    """
    Averages a list of MeasuredDatas

    Parameters
    ----------
    measurements : list[MeasuredData]
        The MeasuredDatas to be averaged

    Returns
    -------
    MeasuredData
        The average of all the MeasuredDatas, with the uncertainty propagated
    """
    avg = MeasuredData(0, 0)

    for point in measurements:
        avg += point

    return avg / len(measurements)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
