from datetime import datetime
from plugins import ral, goesprojsci

__author__ = 'tangz'

if __name__ == '__main__':
    sector = 'oklahoma'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160508_CO-KS'
    start = datetime(2016, 5, 7, 14, 0)
    end = datetime(2016, 5, 8, 2, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)

