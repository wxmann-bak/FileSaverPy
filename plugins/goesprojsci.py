from datetime import datetime, timedelta
import logging
import re
import files
import saver

__author__ = 'tangz'

def savegoesprojsci(sector, savelocation, start, end, interval=timedelta(minutes=12)):
    filename = '{0}{1}_visSave_{2}.log'.format(files.withslash(savelocation), sector,
                                               datetime.utcnow().strftime('%Y%m%d_%H%M'))
    logging.basicConfig(filename=filename, level=logging.INFO)

    thesaver = getbatchsaver(interval, start, end)
    url = "http://goes.gsfc.nasa.gov/goeseast/{0}/vis/".format(sector)
    mutator = lambda x: '{0}_{1}_{2}'.format('vis', sector, x)
    thesaver.saveall(url, savelocation, mutator)

def getbatchsaver(interval, start, end):
    timeconfig = saver.TimeConfig(interval, start, end)
    return saver.BatchSaver(exts=['tif'], timeextractor=goesgsfc_timeextr, timeconfig=timeconfig)

def goesgsfc_timeextr(file):
    regex = '\d{10}'
    dateformat = '%y%m%d%H%M'
    datestr = re.search(regex, file).group(0)
    return datetime.strptime(datestr, dateformat)
