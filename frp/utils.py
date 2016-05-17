# TODO (TS 2016-05-17) Document these functions.

def identity(x):
    return x


def always(x):
    def f(*args, **kwargs):
        return x
    return f


def not_(b):
    return not b


def is_none(x):
    return x is None


def cmp(f1, f2):
    def f(*args, **kwargs):
        return f1(f2(*args, **kwargs))
    return f


def first(xs):
    return None if not xs else next(iter(xs))
