from collections import namedtuple

source = namedtuple('source', [
    'filename',
    'url',
    'ext',
    'timestamp'
])

result = namedtuple('result', [
    'src',
    'saveloc',
    'status'
])


class _StatusCode(object):
    _CODES = {
        'ok': 0,
        'fail': -1
    }

    def __init__(self):
        pass

    def __getattr__(self, item):
        return _StatusCode._CODES[item.lower()]


status = _StatusCode()
