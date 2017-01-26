import functools


class Pipeline(object):
    def __init__(self, *args):
        self._ordered_funcs = reversed(args)

    def __call__(self, arg):
        composed_func = _compose(*self._ordered_funcs)
        return composed_func(arg)


def _compose(*funcs):
    """
    Returns a function that is a composition of the supplied functions.
    For example, compose(f, g, h)(x) == f(g(h(x))).

    :param funcs: functions to compose
    :return: a function that is a composition of funcs
    """
    def compose_pairwise(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose_pairwise, funcs, lambda x: x)
