from .util import *
from .environment import Environment
from .antlr_build.ExprParser import ExprParser

operators = {
    '+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y,
    '^': lambda x, y: x ** y,
    '=': lambda x, y: x == y, '!=': lambda x, y: x != y,
    '>': lambda x, y: x > y, '<': lambda x, y: x < y, '>=': lambda x, y: x >= y, '<=': lambda x, y: x <= y,
    'and': lambda x, y: x and y, 'or': lambda x, y: x or y,
    '.': lambda x, y: getattr(x, y),
    '|': lambda x, y: x.append(y) or x
}

def binary_operator(interpreter, context):
    operator = get_str(context, 1)
    left = get_eval(interpreter, context, 0)
    right = get_eval(interpreter, context, 2)

    if operator not in operators:
        raise RuntimeError("Binary operator '{}' does not exist".format(operator))

    return operators[operator](left, right)


def index_list(list_: list, index):
    return list_[int(index)]


def anonymous_fn(interpreter, parameters, body):
    curr_env = interpreter.env

    def anon(*args):
        last_env = interpreter.env
        env = {}
        new_env = Environment(parent = curr_env, values=env)

        # store all passed arguments in function environment under parameter names
        for i in range(0, count(parameters), 2):  # go by two, b/c commas delimit parameters
            env[get_str(parameters, i)] = args[i // 2]

        interpreter.env = new_env  # add function environment to environment stack

        result = get_eval(interpreter, body)

        interpreter.pop_env()  # remove environment from stack, now that function is done
        interpreter.env = last_env

        return result

    return anon


def handle_function_call(interpreter, context):
    fn = get_eval(interpreter, context, 0)

    if get_str(context, 1) == "`":
        # image call
        args = get(context, 3)
        args = [get_eval(interpreter, args, i) for i in range(0, count(args), 2)]
        result = []

        if len(args) > 0:
            for i in range(len(args[0])):
                curr_args = [x[i] for x in args]
                result.append(fn(*curr_args))

        return result
    else:
        # normal call
        args = get(context, 2)
        args = [get_eval(interpreter, args, i) for i in range(0, count(args), 2)]

        return fn(*args)


def handle_starred_function_call(interpreter, context):
    return_stars = len(get_str(context, 1))

    fn = get_eval(interpreter, context, 0)

    pargs = get(context, 3)
    pargs = [get(pargs, i) for i in range(0, count(pargs), 2)]

    arg_v = [get_eval(interpreter, parg, 1) for parg in pargs]
    arg_s = [len(get_str(parg, 0)) for parg in pargs]
    
    if max(arg_s) != return_stars:
        raise RuntimeError("Return level must match highest input level")
    
    model = arg_v[arg_s.index(return_stars)]

    result = []

    def run_fn(depth, args, curr_result, curr_model):
        if depth == return_stars:
            curr_result.append(fn(*args))
        else:
            new_result = []
            curr_result.append(new_result)

            for i in range(len(curr_model)):
                new_args = []

                for j, arg in enumerate(args):
                    if arg_s[j] > depth:
                        new_args.append(arg[i])
                    else:
                        new_args.append(arg)

                run_fn(depth + 1, new_args, new_result, curr_model[i])
    
    run_fn(0, arg_v, result, model)

    if len(result) == 1:
        result = result[0]

    return result

def handle_expression(interpreter, context):
    expression_len = count(context)

    if expression_len == 3:
        # is wrapping parenthesis?
        if get_str(context, 0) == "(":
            return get_eval(interpreter, context, 1)

        # if not, must be a binary operator
        return binary_operator(interpreter, context)

    elif expression_len == 4:
        if get_str(context, 1) == "[":
            # list[index]
            return index_list(get_eval(interpreter, context, 0), get_eval(interpreter, context, 2))
        elif get_str(context, 2) == ") ->":
            # (params) -> block
            return anonymous_fn(interpreter, get(context, 1), get(context, 3))
        elif get_str(context, 1) == "(":
            # var(args)
            return handle_function_call(interpreter, context)

    elif expression_len == 5:
        if get_str(context, 1) == "`":
            # var`(args)
            return handle_function_call(interpreter, context)
        elif isinstance(get(context, 1), ExprParser.StarsContext):
            return handle_starred_function_call(interpreter, context)

    elif expression_len == 2:
        if get_str(context, 0) == "#":
            # #expr
            return len(get_eval(interpreter, context, 1))

    elif expression_len == 1:
        # if the expression has only one token, it's probably a datatype
        return get_eval(interpreter, context, 0)

    raise RuntimeError("Failed to handle expression: {}".format(context.getText()))