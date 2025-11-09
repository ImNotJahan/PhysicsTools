from .antlr_build.ExprParser import ExprParser

from .util import *

def handle_block(interpreter, context, output_expr: bool):
    for i in range(count(context)):
        child = get(context, i)

        result = get_eval(interpreter, child)

        if output_expr and isinstance(child, ExprParser.ExprContext) and result is not None:
            print(result)
        elif result is not None:
            assert len(result) > 0

            if result[0] == "return":
                if len(result) == 2:
                    return result[1]

    return None