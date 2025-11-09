from physics_utils import MeasuredData

import numpy

def steps(x: MeasuredData, *options) -> str:
    option_count = len(options)

    plug_in = True
    trunc   = True
    method  = "composite"
    calc    = "uncertainty"

    if option_count > 3:
        trunc = options[3]
    if option_count > 2:
        plug_in= options[2]
    if option_count > 1:
        method = options[1]
    if option_count > 0:
        calc = options[0]

    if method == "composite":
        return x.all_steps_composite(plug_in, trunc)[int(calc == "uncertainty")]
    else:
        return '\n'.join(x.all_steps_sequential(plug_in, trunc)[int(calc == "uncertainty")])

def std(data: list[MeasuredData]) -> MeasuredData:
    return MeasuredData(
        float(numpy.std(list(map(float, data)))),
        0
    )