__author__ = 'tangz'


class TimeConfig(object):
    # interval < 0 means that images must not have the same timing
    def __init__(self, interval, start=None, end=None):
        self.interval = interval
        if start and end and start > end:
            raise ValueError("Start time: {0} > end time: {1}".format(start, end))
        self.start = start
        self.end = end


def passestime(urlsrc, timeconfig, hist):
    if not timeconfig or not urlsrc.timestamp:
        return True

    if timeconfig.start and timeconfig.end:
        rangepasses = timeconfig.start <= urlsrc.timestamp <= timeconfig.end
    elif timeconfig.start:
        rangepasses = timeconfig.start <= urlsrc.timestamp
    elif timeconfig.end:
        rangepasses = urlsrc.timestamp <= timeconfig.end
    else:
        rangepasses = True

    if not hist:
        intervalpasses = True
    elif urlsrc.timestamp in [hist_save.timestamp for hist_save in hist]:
        intervalpasses = False
    elif timeconfig.interval:
        dt = urlsrc.timestamp - hist[-1].timestamp
        intervalpasses = dt >= timeconfig.interval
    else:
        intervalpasses = True

    return rangepasses and intervalpasses