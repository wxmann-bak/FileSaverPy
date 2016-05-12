from datetime import datetime
from plugins import ral

__author__ = 'tangz'

if __name__ == '__main__':
    station = 'KDLH'
    saveloc = 'C:\\Users\\tangz\\Documents\\pythontest'
    start = datetime(2016, 5, 10, 12, 0)
    end = datetime(2016, 5, 10, 13, 0)
    ral.savefromral(station, saveloc, start, end)

