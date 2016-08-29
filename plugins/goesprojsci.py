from datetime import datetime, timedelta
import re

from core import files, timing
from savers import batch

__author__ = 'tangz'


def savegoesprojsci(sector, savelocation, start, end, interval=timedelta(minutes=12)):
    thesaver = getbatchsaver(interval, start, end)
    url = "http://goes.gsfc.nasa.gov/goeseast/{0}/vis/".format(sector)
    mutator = lambda x: '{0}_{1}_{2}'.format('vis', sector, x)
    thesaver.saveall(url, savelocation, mutator)


def savegoesprojsci2(savelocation, start, end, interval=timedelta(hours=1), older=True):
    thesaver = getbatchsaver(interval, start, end, ext='jpg')
    url = "http://goes.gsfc.nasa.gov/goescolor/goeseast/hurricane2/color_med/"
    if older:
        url += "older_images/"
    mutator = lambda x: '{0}_{1}'.format('sat', x)
    thesaver.saveall(url, savelocation, mutator)


def getbatchsaver(interval, start, end, ext='tif'):
    timeconfig = timing.TimeConfig(interval, start, end)
    removelatest = lambda file: 'latest' not in file
    return batch.BatchSaver(exts=[ext], filter=removelatest, timeextractor=goesgsfc_timeextr, timeconfig=timeconfig)


def goesgsfc_timeextr(file):
    regex = '\d{10}'
    dateformat = '%y%m%d%H%M'
    datepattern = re.search(regex, file)
    if not datepattern:
        raise files.InvalidResourceError("Cannot find date-time for file: {0}".format(file))
    return datetime.strptime(datepattern.group(0), dateformat)
