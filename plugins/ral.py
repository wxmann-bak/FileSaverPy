from datetime import datetime
import re
from savers import batch

from core import timing

__author__ = 'tangz'


def savefromral(station, savelocation, start, end, interval=None):
    thesaver = getbatchsaver(interval, start, end)
    url = "http://weather.rap.ucar.edu/radar/nws_nids/BREF1/" + station
    mutator = lambda x: station + '_' + x
    thesaver.saveall(url, savelocation, mutator)


def getbatchsaver(interval, start, end, bg='black'):
    timeconfig = timing.TimeConfig(interval, start, end)
    return batch.BatchSaver(exts=['png'], filter=lambda x: bg in x,
                            timeextractor=ral_timeextractor, timeconfig=timeconfig)


def ral_timeextractor(file):
    regex = "\d{8}_\d{6}"
    dateformat = '%Y%m%d_%H%M%S'
    datetimestr = re.search(regex, file).group(0)
    return datetime.strptime(datetimestr, dateformat)