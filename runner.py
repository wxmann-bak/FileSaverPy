from datetime import datetime, timedelta
from plugins import ral, goesprojsci

__author__ = 'tangz'

def save_ral_radar():
    station = "KICT"
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160525_KS-OK-SD-IA-MN'
    start = datetime(2016, 5, 25, 22, 27)
    end = datetime(2016, 5, 26, 5, 56)
    ral.savefromral(station, saveloc, start=start, end=end)


def save_goesproj_vis():
    sector = 'oklahoma'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160525_KS-OK-SD-IA-MN'
    start = datetime(2016, 5, 25, 14, 0)
    end = datetime(2016, 5, 26, 2, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)

if __name__ == '__main__':
    save_goesproj_vis()



