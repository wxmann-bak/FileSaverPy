import re
from datetime import datetime

from core import web


def current_time(tz=None):
    return datetime.now(tz=tz)


def current_utc():
    return datetime.utcnow()


def start_end_filter(start=None, end=None):
    def thefilter(timestamp):
        if start and end:
            return start <= timestamp <= end
        elif start:
            return start <= timestamp
        elif end:
            return timestamp <= end
        else:
            return True
    return thefilter


### Time extractor ###


def regex_timeextractor(regex, dateformat):
    def theextractor(file):
        datepattern = re.search(regex, file)
        if not datepattern:
            raise web.InvalidResourceError("Cannot find date-time for file: {0}".format(file))
        return datetime.strptime(datepattern.group(0), dateformat)
    return theextractor
