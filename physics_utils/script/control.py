from .util import *

def handle_control(interpreter, context):
    keyword = get_str(context, 0)

    if keyword == "return":
        if count(context) == 1:
            return ["return"]

        return ["return", get_eval(interpreter, context, 1)]

    return None