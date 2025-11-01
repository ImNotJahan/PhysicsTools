# Getting started
## Installation
`physics_utils` can be installed straight from PyPI using pip, like so:
```batch
python3 -m pip install physics-utils
```

## Usage
At the center of this package is the `MeasuredData` class, 
which represents a data point with uncertainty. Most of the 
features in this package will use and expect `MeasuredData` objects
for inputs and outputs. They can be quickly imported from either
`physics_utils` or `physics_utils.data`, but due to their 
prominence the prior is prefered. API reference for them, however, is
found under the `physics_utils.data` section.

Here's an example using `MeasuredData` to perform a quick calculation 
with uncertainty:

```python
from physics_utils import MeasuredData

# we recorded 5 seconds, however our timer only goes up to the tenth of a second
# thus the reading error of 0.1
time = MeasuredData(5, 0.1) 
# measured in centimeters
# our ruler only goes up to the millimeter
distance = MeasuredData(197.5, 0.1)

# let's quickly convert distance to meters...
distance /= 100
# distance = 1.975±0.001

# now let's calculate the velocity in m/s
velocity = distance / time

print(velocity) # 39.5±0.8
```

For graphing, check out the `physics_utils.graph` module; 
and for tables, the `physics_utils.table` module.