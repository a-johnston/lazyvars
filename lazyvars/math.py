import math
from lazyvars.variable import Variable


def log(x):
    if isinstance(x, Variable):
        return Variable(
            value=lambda: log(x.get_value()),
            __varid__=int(math.log(x.__varid__)),
            __vars__=Variable.__get_subvars__(x),
        )
    return math.log(x)
