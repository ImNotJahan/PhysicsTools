import math
import numpy as np
import pandas as pd

class MeasuredData:
    def __init__(self, measurement: float, reading_error: float, standard_error=0.0):
        self.value = measurement
        self.reading_error = reading_error
        self.standard_error = standard_error

    def error(self):
        """
        Returns the larger error of the data
        >>> MeasuredData(100.2, 2.4, 10.12).error()
        10.12
        """
        return max(self.reading_error, self.standard_error)

    def __int__(self):
        """
        Returns the value of this point as an integer
        >>> int(MeasuredData(100.2, 2, 10))
        100
        """
        return int(self.value)

    def __float__(self):
        """
        Returns the value of this point as a float
        >>> float(MeasuredData(100.2, 2, 10))
        100.2
        """
        # we still wrap it in a float conversion
        # just incase the provided value for the
        # data point was an int or something
        return float(self.value)

    def avg_from_set(measurements: list[float], reading_error: float) -> object:
        n = len(measurements)
        average = sum(measurements) / n
        standard_deviation = math.sqrt(
            (1 / (n - 1)) * sum(([(x - average)**2 for x in measurements]))
        )
        return MeasuredData(average, reading_error, standard_deviation / math.sqrt(n))

    def from_set(measurements: list[float], reading_error: float, standard_error=0.0) -> list:
        return [MeasuredData(x, reading_error, standard_error) for x in measurements]

    def __add__(self, other):
        """
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
                error(self.standard_error, self.standard_error)
            )

        return MeasuredData(self.value + other, self.reading_error, self.standard_error)

    def __sub__(self, other):
        if isinstance(other, MeasuredData):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return MeasuredData(
                self.value - other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, self.standard_error)
            )

        return MeasuredData(self.value - other, self.reading_error, self.standard_error)

    def __mul__(self, other):
        if isinstance(other, MeasuredData):
            def error(sx, sy) -> float:
                return (
                            (self.value * other.value) *
                            math.sqrt (
                                (sx / self.value) ** 2 +
                                (sy / other.value) ** 2
                            )
                        )

            return MeasuredData(
                self.value * other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: (self.value * other) * (s / self.value)

        return MeasuredData(self.value * other, error(self.reading_error), error(self.standard_error))

    def __truediv__(self, other):
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

        error = lambda s: (self.value / other) * (s / self.value)

        return MeasuredData(self.value / other, error(self.reading_error), error(self.standard_error))

    def __pow__(self, other: int):
        error = lambda s: other * self.value ** (other - 1) * s

        return MeasuredData(
            self.value ** other,
            error(self.reading_error),
            error(self.standard_error)
        )

    def sine(self):
        error = lambda s: s * math.cos(self.value)

        return MeasuredData(
            math.sin(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def cosine(self):
        error = lambda s: s * math.sin(self.value)

        return MeasuredData(
            math.cos(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def tangent(self):
        return self.sine() / self.cosine()

    def __str__(self):
        """
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

# from here on out we have some utility functions
def csv_to_numpy(file_name: str, rotate=False) -> np.ndarray:
    if rotate:
        return pd.read_csv(file_name).T.to_numpy()
    return pd.read_csv(file_name).to_numpy()


def remove_nan(data_points: np.ndarray):
    return [x for x in data_points if not np.isnan(x)]


def remove_nan_2d(data_points: np.ndarray):
    return [remove_nan(x) for x in data_points]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
