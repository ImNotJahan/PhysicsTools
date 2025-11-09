from physics_utils.data import math

from .builtin import steps, std

class Environment:
    def __init__(self, parent=None, values=None):
        self.parent = parent

        if values is None: self.values = {}
        else:              self.values = values

    def get(self, variable: str):
        if variable in self.values:
            return self.values[variable]

        if self.parent:
            return self.parent.get(variable)

        raise RuntimeError("Unknown variable \"{}\"".format(variable))

    def add(self, variable: str, value):
        self.values[variable] = value

variables = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "arcsin": math.asin, "arctan": math.atan,
    "exit": exit, "print": print, "steps": steps, "std": std,
    "true": True, "false": False, "nil": None
}

default_environment = Environment(values=variables)