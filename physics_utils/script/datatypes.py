from .util import *
from physics_utils import MeasuredData
from .antlr_build.ExprParser import ExprParser

def make_list(interpreter, context) -> list:
    result = []

    for i in range(1, count(context) - 1, 2):
        result.append(get_eval(interpreter, context, i))

    return result


def make_number(context) -> MeasuredData:
    numeric_parts = list(map(lambda x: float(x.getText()), context.getTokens(ExprParser.FLOAT)))

    if len(numeric_parts) == 0:
        raise RuntimeError("Number had no numeric parts")

    if len(numeric_parts) == 1:  # first part corresponds to value
        return MeasuredData(numeric_parts[0], 0)
    # second part (if exists) corresponds to uncertainty
    return MeasuredData(numeric_parts[0], numeric_parts[1])


def make_string(context) -> str:
    return get_str(context, 0)[1:-1]


def make_symbol(context) -> str:
    return get_str(context)

def make_package(context) -> str:
    return get_str(context)