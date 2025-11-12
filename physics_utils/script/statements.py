from .antlr_build.ExprParser import ExprParser
from physics_utils import MeasuredData
from .util import *
from .expressions import anonymous_fn
from importlib import import_module

def assignment(interpreter, variable: str, value) -> None:
    interpreter.env.add(variable, value)

    if isinstance(value, MeasuredData):
        value.label = variable


def uncertainty_assignment(interpreter, variable: str, uncertainty: MeasuredData) -> None:
    interpreter.env.get(variable).reading_error = uncertainty.value


def list_assignment(interpreter, list_: list, index: MeasuredData, value) -> None:
    list_[int(index)] = value


def handle_if(interpreter, context) -> None:
    # if expr then block (else if expr then block)* (else block)? end if

    statement_len = count(context)

    condition_offset = 1
    body_offset = 3

    # handle beginning if statement
    if get_eval(interpreter, context, condition_offset):
        # cond was true, so execute block
        get_eval(interpreter, context, body_offset)
    else:
        # if statement was false, so (potentially) evaluate else if and else statements

        has_else = get_str(context, statement_len - 3) == "else"
        # to explain this statement, we subtract 5 since any if statement contains five non-elif tokens
        # (if, expr, then, block, end if), then subtract 2 * has_else, that is, we subtract 2 more if
        # there is an else statement, since that would also add two tokens (else, block). Finally, we
        # divide the remaining token count by 4, since every elif statement has four tokens (else if,
        # expr, then, block)
        elif_count = (statement_len - 5 - 2 * has_else) // 4

        # loop through elif statements
        for i in range(elif_count):
            # that is, where this elif statement starts
            elif_base = 4 + i * 4

            if get_eval(interpreter, context, elif_base + condition_offset):
                get_eval(interpreter, context, elif_base + body_offset)
                # since an elif statement was true, don't execute any other statements in this if
                has_else = False
                break

        if has_else:
            get_eval(interpreter, context, statement_len - 2)


def handle_for(interpreter, context) -> None:
    # for var (in list | from x to y) loop block end loop

    # the "for operator" refers to the keyword used in the for loop to determine the type of for loop, that is,
    # from (denoting a loop in a range) or in (for looping over a list)
    for_op = get_str(context, 2)

    var_name = get_str(context, 1)

    if for_op == "from":
        # get bounds of our range
        left_bound, right_bound = interpreter.visit(context.getChild(3)), interpreter.visit(context.getChild(5))
        left_bound, right_bound = int(left_bound), int(right_bound)

        for i in range(left_bound, right_bound + 1): # loop through inclusive, inclusive
            # pass i into current environment as var
            interpreter.env.add(var_name, MeasuredData(i, 0))

            get_eval(interpreter, context, 7)

    elif for_op == "in":
        # for x in list
        for x in get_eval(interpreter, context, 3):
            interpreter.env.add(var_name, x)

            get_eval(interpreter, context, 5)

    else:
        raise RuntimeError("Unknown for operator \"{}\"".format(for_op))


def handle_while(interpreter, context) -> None:
    # while expr loop block end loop

    while get_eval(interpreter, context, 1):
        get_eval(interpreter, context, 3)


def handle_define(interpreter, context) -> None:
    # define var(params) as block end var

    fn_name = get_str(context, 1)

    if fn_name != get_str(context, 8):
        raise RuntimeError(
            "Function should end with \"end {}\", ends with \"end {}\" instead"
            .format(fn_name, get_str(context, 8))
        )

    # we create an anonymous function, and then just give it a name
    fn = anonymous_fn(interpreter, get(context, 3), get(context, 6))

    # add fn to environment
    interpreter.env.add(fn_name, fn)


def handle_import(interpreter, context) -> None:
    if get_str(context, 0) == "import":
        # import var
        package_name = get_str(context, 1)
        package = import_module(package_name)

        interpreter.env.add(package_name, package)

    elif get_str(context, 0) == "from":
        # from var import var (, var)*
        package_name = get_str(context, 1)
        package = import_module(package_name)

        for i in range(3, count(context), 2):
            part_name = get_str(context, i)
            interpreter.env.add(part_name, getattr(package, part_name))



def handle_statement(interpreter, context):
    parts = context.getChildCount()

    assert parts != 0

    keyword = context.getChild(0).getText()

    if parts == 3:
        # statements of this length typically have an operator in the middle
        operator = get_str(context, 1)

        if operator == ":=":
            # var := expr
            assignment(interpreter, get_str(context, 0), get_eval(interpreter, context, 2))
        elif operator == ":~":
            # var := expr
            uncertainty_assignment(interpreter, get_str(context, 0), get_eval(interpreter, context, 2))

    elif parts == 5:
        if get_str(context, 3) == "] :=":
            # list[index] := expr
            list_assignment(interpreter, get_eval(interpreter, context, 0), get_eval(interpreter, context, 2), get_eval(interpreter, context, 4))

    if keyword == "if":
        handle_if(interpreter, context)
    elif keyword == "for":
        handle_for(interpreter, context)
    elif keyword == "while":
        handle_while(interpreter, context)
    elif keyword == "define":
        handle_define(interpreter, context)
    elif keyword == "import" or keyword == "from":
        handle_import(interpreter, context)

    elif isinstance(get(context, 0), ExprParser.CtrlContext):
        return get_eval(interpreter, context, 0)

    return None