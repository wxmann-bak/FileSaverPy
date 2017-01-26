import operator


def valid_exts(*exts):
    allowed_exts = [ext.replace('.', '') for ext in exts]

    def test_ext(src):
        return src.ext in allowed_exts
    return test_ext


def min_divisible_by(num):
    if num <= 0:
        raise ValueError("Divisble by number must be > 0.")

    def test_minute(src):
        src_min = src.timestamp.minute
        return src_min % num == 0
    return test_minute


def time_in_range(min_time=None, max_time=None, inclusive=True):
    has_min_time = min_time is not None
    has_max_time = max_time is not None

    if has_min_time and has_max_time and min_time > max_time:
        raise ValueError("Max time must be after Min time")

    op = operator.le if inclusive else operator.lt

    def test_time(src):
        srctime = src.timestamp
        if has_min_time and has_max_time:
            return op(min_time, srctime) and op(srctime, max_time)
        elif has_min_time:
            return op(min_time, srctime)
        elif has_max_time:
            return op(srctime, max_time)
        else:
            return True
    return test_time


def name_contains(substr):
    return lambda src: substr in src.filename



