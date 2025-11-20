from .util import *

class Break(Exception):
    def __init__(self):
        # If this error is caught inside of a loop (as it should,) then this
        # message is never printed. Otherwise, it points out the issue.
        super().__init__("Break placed outside of loop")

class Continue(Exception):
    def __init__(self):
        super().__init__("Continue placed outside of loop")

def handle_control(interpreter, context):
    keyword = get_str(context, 0)

    if keyword == "return":
        if count(context) == 1:
            return ["return"]

        return ["return", get_eval(interpreter, context, 1)]

    if keyword == "break":
        raise Break()
    
    if keyword == "continue":
        raise Continue()

    return None