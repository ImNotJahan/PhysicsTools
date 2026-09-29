import math
from .measureddata import MeasuredData
import pandas as pd
import numpy as np
from numpy import std

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
    Averages a list of floats all having the same reading error

    Parameters
    ----------
    measurements : list[float]
        The measurements to be averaged
    reading_error : float
        The error which all of the measurements share

    Returns
    -------
    MeasuredData
        The mean of the measurements. The reading error is kept as given, since the readings may share a
        systematic offset. The standard error is the sample standard deviation (n - 1) divided by sqrt(n).
    """
    n = len(measurements)
    average = sum(measurements) / n
    standard_error = float(std(measurements, ddof=1) / math.sqrt(n)) if n > 1 else 0.0
    return MeasuredData(average, reading_error, standard_error)

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
        The mean of the values. The reading error is the individual reading errors added in quadrature and divided
        by n, and the standard error is the sample standard deviation (n - 1) divided by sqrt(n).
    """
    values = [float(x) for x in measurements]

    n = len(values)
    average = sum(values) / n
    reading_error = math.sqrt(sum(x.reading_error ** 2 for x in measurements)) / n
    standard_error = float(std(values, ddof=1) / math.sqrt(n)) if n > 1 else 0.0
    return MeasuredData(average, reading_error, standard_error)
