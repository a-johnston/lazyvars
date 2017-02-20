class Session:
    def __init__(self):
        self.__vars__ = {}

    def __getattr__(self, name):
        if name not in self.__vars__:
            self.__setattr__(name, None)
        return self.__vars__[name]

    def __setattr__(self, name, value):
        if name is '__vars__':
            super().__setattr__(name, value)
        elif name in self.__vars__:
            self.__vars__[name].set_value(value)
        else:
            self.__vars__[name] = value if isinstance(value, Variable) else Variable(value)

    def __call__(self, **kwargs):
        to_eval = set(self.__vars__) - set(kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        return dict(zip(to_eval, [self.__getattr__(n).get_value() for n in to_eval]))

class Variable:
    __override__ = [
        '__add__',
        '__sub__',
        '__mul__',
        '__truediv__',
        '__floordiv__',
        '__mod__',
        '__pow__',
        '__le__',
        '__ge__',
        '__lt__',
        '__gt__',
    ]

    def __init__(self, value=None, __varid__=None, __vars__=None):
        self.set_value(value)
        self.__varid__ = __varid__ or id(self)
        self.__vars__ = __vars__

    def __hash__(self):
        return id(self)

    def __operator__(self, x, op):
        return Variable(
            value=lambda: Variable.__unpack__(self).__getattribute__(op)(Variable.__unpack__(x)),
            __varid__=lambda: Variable.__get_vid__(self).__getattribute__(op)(Variable.__get_vid__(x)),
            __vars__=Variable.__get_subvars__(self) + Variable.__get_subvars__(x),
        )

    def __eq__(self, x):
        if isinstance(x, Variable):
            return Variable.__get_vid__(self) == Variable.__get_vid__(x)
        return self.get_value() == x

    def __is_constant__(self):
        return not callable(self.__value__) and self.__value__ is not None

    def __is_unbound__(self):
        return self.__value__ is None

    def set_value(self, value):
        self.__value__ = value;

    def get_value(self):
        return Variable.__unpack__(self)

    @staticmethod
    def __unpack__(x):
        if isinstance(x, Variable):
            if x.__is_constant__():
                return x.__value__
            if callable(x.__value__):
                r = x.__value__()
                if isinstance(r, Variable):
                    return x if x == r else r
                return r
        return x

    @staticmethod
    def __get_vid__(x):
        if isinstance(x, Variable):
            if callable(x.__varid__):
                return x.__varid__()
            elif x.__value__ is None:
                return x.__varid__
            else:
                return Variable.__get_vid__(x.get_value())
        return hash(x)

    @staticmethod
    def __get_subvars__(x):
        if isinstance(x, Variable):
            if not callable(x.__value__):
                return [x]
            return x.__vars__
        return []


for method in Variable.__override__:
    (lambda a: setattr(Variable, method, lambda x, y: x.__operator__(y, a)))(method)
del Variable.__override__
