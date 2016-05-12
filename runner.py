from datetime import datetime
import logging
from plugins import ral

__author__ = 'tangz'

if __name__ == '__main__':
    filename = 'logs/Save-{0}.log'.format(datetime.utcnow().strftime('%Y%m%d_%H%M'))
    logging.basicConfig(filename=filename, level=logging.INFO)
    station = 'KTLX'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160509_OK-TX-AR-KS-NE-IA'
    start = datetime(2016, 5, 9, 20, 0)
    end = datetime(2016, 5, 10, 1, 0)
    ral.savefromral(station, saveloc, start, end)

