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
        The average of all the measurements, with the uncertainty propagated
    """
    n = len(measurements)
    average = sum(measurements) / n
    standard_deviation = float(std(measurements))
    return MeasuredData(average, reading_error, standard_deviation)

def avg_measured_datas(measurements: list[MeasuredData]) -> MeasuredData:
    import math
    """
    Averages a list of MeasuredDatas

    Parameters
    ----------
    measurements : list[MeasuredData]
        The MeasuredDatas to be averaged

    Returns
    -------
    MeasuredData
        The average of all the MeasuredDatas, with the standard error being
        the standard deviation.
    """
    values = [float(x) for x in measurements]

    n = len(values)
    average = sum(values) / n
    standard_deviation = float(std(values))
    return MeasuredData(average, 0, standard_deviation)