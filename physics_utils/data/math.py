"""
Redefines some math functions to add support for MeasuredDatas
"""

from .measureddata import MeasuredData
import math

def sin(x: float | MeasuredData) -> float | MeasuredData:
    if isinstance(x, MeasuredData):
        return x.sine()
    return math.sin(x)

def cos(x: float | MeasuredData) -> float | MeasuredData:
    if isinstance(x, MeasuredData):
        return x.cosine()
    return math.cos(x)

def tan(x: float | MeasuredData) -> float | MeasuredData:
    if isinstance(x, MeasuredData):
        return x.tangent()
    return math.tan(x)

def asin(x: float | MeasuredData) -> float | MeasuredData:
    if isinstance(x, MeasuredData):
        return x.arcsin()
    return math.asin(x)

def atan(x: float | MeasuredData) -> float | MeasuredData:
    if isinstance(x, MeasuredData):
        return x.arctan()
    return math.asin(x)