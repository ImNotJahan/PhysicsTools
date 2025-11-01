# The data module

The data module adds the `MeasuredData` class for working with values 
with uncertainty, add ands a number of helper functions to use with 
it.

## Using MeasuredData
To create a `MeasuredData` object, you just need to provide a value and an 
error, like so:
```python
from physics_utils import MeasuredData
# or, you could do
# from physics_utils.data import MeasuredData

# creates an object with a value of 7 and a
# reading error of 0.5
point = MeasuredData(7, 0.5)

print(point) # 7±0.5
```

Once you've created a `MeasuredData` object, you can treat it as any 
other numerical value, and perform whatever calculations you need to
using it. The error will be automatically propagated as you do so.

```python
from physics_utils import MeasuredData as MD

mu = MD(-0.00311, 0.00005)
m = MD(0.3057, 0.00005)
x = MD(0.242, 0.0002)

print(mu * 9.81 * m * x) # -0.00226±0.00004 
```

To use trigonometric functions with `MeasuredData` as the argument,
you can use the built in `.sine()` `.cosine()` `.tangent()` `.arcsin()`
and `.arctan()` methods on a `MeasuredData` object. Note that this will
treat the `MeasuredData` as being in radians.

## Averaging methods
The data module also provides methods for quickly averaging a bunch of
measurements from the same device that have the same reading error,
using the `avg_from_set` function; and for averaging a list of `MeasuredData`,
using the `avg_measured_datas` function.