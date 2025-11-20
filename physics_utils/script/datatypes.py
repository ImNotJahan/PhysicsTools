from .util import *
from physics_utils import MeasuredData
from .antlr_build.ExprParser import ExprParser

def make_list(interpreter, context) -> list:
    result = []

    for i in range(1, count(context) - 1, 2):
        result.append(get_eval(interpreter, context, i))

    return result


def make_number(context) -> MeasuredData:
    numeric_parts = [n.getText().split("*") for n in context.SCI_NUM()]

    magnitude_to_int = lambda mag: int(mag.split("^")[1])

    if len(numeric_parts) == 0:
        raise RuntimeError("Number had no numeric parts")

    value = 0
    uncertainty = 0

    value = float(numeric_parts[0][0])
    
    if len(numeric_parts[0]) > 1:
        value *= 10 ** magnitude_to_int(numeric_parts[0][1])

    if len(numeric_parts) == 2:
        # second part (if exists) corresponds to uncertainty
        uncertainty = float(numeric_parts[1][0]) # first part would be float

        # if there is a second part to the number, it would be the magnitude
        if len(numeric_parts[1]) > 1:
            uncertainty *= 10 ** magnitude_to_int(numeric_parts[1][1])

    return MeasuredData(value, uncertainty)


def make_string(context) -> str:
    return get_str(context, 0)[1:-1]


def make_symbol(context) -> str:
    return get_str(context)

def make_package(context) -> str:
    return get_str(context)