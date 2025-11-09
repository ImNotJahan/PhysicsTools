[![PyPI - Version](https://img.shields.io/pypi/v/physics-utils)](https://pypi.org/project/physics-utils/)
[![Static Badge](https://img.shields.io/badge/docs-blue)](https://physics-utils.readthedocs.io)
[![Python Tests](https://github.com/ImNotJahan/PhysicsTools/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ImNotJahan/PhysicsTools/actions/workflows/python-tests.yml)

# PhysicsTools
This is a library for dealing with some tedious tasks for basic physics labs.

## Features
* Automatic uncertainty propagation on basic arithmetic and trigonometric operations
* Generated LaTeX steps of any calculations done with the `MeasuredData` class
* A physics scripting language for fast usage of the library
* Graping wrappers that take numbers with uncertainty for automatic error bars
* LaTeX data table generators

## Installation
Look under the examples folder to see the library in use.

`physics_utils` can be installed straight from PyPI using pip, like so:
```batch
python3 -m pip install physics-utils
```

## Usage
To get started with using the library, you can import `MeasuredData` from `physics_utils` and begin doing
calculations like normal once your numbers are wrapped:
```python
from physics_utils import MeasuredData

print(MeasuredData(2, 0.5) * MeasuredData(3, 0.4)) # 6±2.
```

To start using the scripting language, you can type `python3 -m physics_utils.script` in your terminal to start the
interpreter, or `python3 -m physics_utils.script <filename>` to run a file. To do the same as the example above in the
physics script interpreter, you'd just need to type this:
```
>>> 2~0.5 * 3~0.4
6±2.
```

And there are a number of other helpful features built into the language.

For more information on using the package, take a look at the [documentation](https://physics-utils.readthedocs.io) and
[examples](https://github.com/ImNotJahan/PhysicsTools/tree/main/examples).