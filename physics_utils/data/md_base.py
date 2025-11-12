
import math
import numpy as np
from typing import Iterable, Self, Any

safe_div = lambda x, y: 0 if y == 0 else x / y

class MeasuredDataBase:
    value = 0
    reading_error = 0
    standard_error = 0

    def _new(self, measurement: float, reading_error: float, standard_error=0.0):
        return type(self)(measurement, reading_error, standard_error)

    def error(self) -> float:
        """
        Returns the uncertainty on the data, which is taken to be the greatest error it has

        Examples
        --------
        >>> MeasuredDataBase(100.2, 2.4, 10.12).error()
        10.12
        """
        return max(abs(self.reading_error), abs(self.standard_error))

    def __int__(self) -> int:
        """
        Returns the value of this point truncated to an integer

        Examples
        --------
        >>> int(MeasuredDataBase(100.2, 2, 10))
        100
        """
        return int(self.value)

    def __float__(self) -> float:
        """
        Returns the value of this point as a float

        Examples
        --------
        >>> float(MeasuredDataBase(100.2, 2, 10))
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
        >>> print(MeasuredDataBase(10.4, 0.0, 0.5) + MeasuredDataBase(3.0, 1.0, 0.2))
        13.0±1.
        >>> print(MeasuredDataBase(12.34, 0.05, 0.02) + 10.111)
        22.45±0.05
        """
        if isinstance(other, MeasuredDataBase):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return self._new(
                self.value + other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        return self._new(self.value + other, self.reading_error, self.standard_error)

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
        if isinstance(other, MeasuredDataBase):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return self._new(
                self.value - other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        return self._new(self.value - other, self.reading_error, self.standard_error)

    def __rsub__(self, other) -> Self:
        """
        Support for subtraction with a MeasuredData as the right operand
        """
        if isinstance(other, MeasuredDataBase):
            error = lambda x, y: math.sqrt(x ** 2 + y ** 2)
            return self._new(
                other.value - self.value,
                error(other.reading_error, self.reading_error),
                error(other.standard_error, self.standard_error)
            )

        return self._new(other - self.value, self.reading_error, self.standard_error)

    def __mul__(self, other) -> Self:
        """
        Support for multiplication with a MeasuredData as the left operand
        """
        if isinstance(other, MeasuredDataBase):
            def error(sx, sy) -> float:
                return (
                            (self.value * other.value) *
                            math.sqrt (
                                safe_div(sx, self.value) ** 2 +
                                safe_div(sy, other.value) ** 2
                            )
                        )

            return self._new(
                self.value * other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: (self.value * other) * safe_div(s, self.value)

        return self._new(self.value * other, error(self.reading_error), error(self.standard_error))

    def __rmul__(self, other) -> Self:
        """
        Support for multiplication with a MeasuredData as the right operand
        """
        # multiplication is symmetric
        return self.__mul__(other)

    def __truediv__(self, other) -> Self:
        """
        Support for division with a MeasuredData as the left operand
        """
        if isinstance(other, MeasuredDataBase):
            def error(sx, sy) -> float:
                return (
                            (self.value / other.value) *
                            math.sqrt (
                                (sx / self.value) ** 2 +
                                (sy / other.value) ** 2
                            )
                        )

            return self._new(
                self.value / other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: (self.value / other) * safe_div(s, self.value)

        return self._new(self.value / other, error(self.reading_error), error(self.standard_error))

    def __rtruediv__(self, other) -> Self:
        """
        Support for division with a MeasuredData as the right operand

        Examples
        --------
        >>> x = MeasuredDataBase(105, 0.1) / MeasuredDataBase(5, 0.5)
        >>> x.value == 21
        True
        """
        if isinstance(other, MeasuredDataBase):
            def error(sx, sy) -> float:
                return (
                        (other.value / self.value) *
                        math.sqrt(
                            (sx / other.value) ** 2 +
                            (sy / self.value) ** 2
                        )
                )

            return self._new(
                other.value / self.value,
                error(other.reading_error, self.reading_error),
                error(other.standard_error, self.standard_error)
            )

        error = lambda s: (other / self.value) * safe_div(s, self.value)

        return self._new(other / self.value, error(self.reading_error), error(self.standard_error))

    def __pow__(self, other) -> Self:
        """
        Support for taking a MeasuredData to some integer power
        """
        if isinstance(other, MeasuredDataBase):
            def error(sx, sy):
                x, y = self.value, other.value
                return math.sqrt((y * x ** (y - 1)) ** 2 * sx ** 2 + (x ** y * math.log(y)) ** 2 * sy ** 2)

            return self._new(
                self.value ** other.value,
                error(self.reading_error, other.reading_error),
                error(self.standard_error, other.standard_error)
            )

        error = lambda s: abs(other * self.value ** (other - 1) * s)

        return self._new(
            self.value ** other,
            error(self.reading_error),
            error(self.standard_error)
        )

    def sine(self) -> Self:
        """
        Takes the result of sin(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: abs(s * math.cos(self.value))

        return self._new(
            math.sin(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def cosine(self) -> Self:
        """
        Takes the result of cos(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: abs(s * math.sin(self.value))

        return self._new(
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

        return self._new(
            math.atan(self.value),
            error(self.reading_error),
            error(self.standard_error)
        )

    def arcsin(self) -> Self:
        """
        Takes the result of arcsin(x) on a MeasuredData with the MeasuredData treated as radians
        """
        error = lambda s: s / math.sqrt(1 - self.value ** 2)

        return self._new(
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
        return self._new(
            abs(self.value),
            self.reading_error,
            self.standard_error
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, MeasuredDataBase):
            return self.value == other.value
        return self.value == other

    def __gt__(self, other) -> bool:
        if isinstance(other, MeasuredDataBase):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other) -> bool:
        return self == other or self > other

    def __str__(self) -> str:
        """
        Converts this MeasuredData into a string representation, showing the value and uncertainty
        The uncertainty is rounded to one digit, and the value is then rounded to the same place as the uncertainty

        Examples
        --------
        >>> str(MeasuredDataBase(1234.56789, 0.05333))
        '1234.57±0.05'
        >>> str(MeasuredDataBase(100.4, 0.0, 4.3))
        '100.0±4.'
        >>> str(MeasuredDataBase(1234.567, 543, 0))
        '1200.0±500.'
        """
        if self.error() == 0:
            return str(self.value)

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

    def __repr__(self) -> str:
        return self.__str__()

    def latex(self, wrap=True) -> str:
        """
        Converts the MeasuredData into a string representation, as described in the __str__ method, but uses the LaTeX
        symbol for ±, and wraps the value in $$
        """
        if self.error() == 0:
            return str(self.value)

        parts = str(self).split("±")
        formatted = "{} \\pm {}".format(parts[0], parts[1])

        if wrap:
            return "${}$".format(formatted)
        return formatted
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
        return [MeasuredDataBase(x, reading_error, standard_error) for x in measurements]
