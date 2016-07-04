from datetime import datetime, timedelta
from plugins import ral, goesprojsci, ssd

__author__ = 'tangz'

def save_ral_radar():
    station = "KRLX"
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160623-24_WVFloods'
    start = datetime(2016, 6, 23, 5, 0)
    end = datetime(2016, 6, 24, 2, 0)
    ral.savefromral(station, saveloc, start=start, end=end, interval=timedelta(minutes=9))


def save_goesproj_vis():
    sector = 'oklahoma'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160525_KS-OK-SD-IA-MN'
    start = datetime(2016, 5, 25, 14, 0)
    end = datetime(2016, 5, 26, 2, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)


def save_ssd_periodic():
    prepend = "Blas-"
    url_avn = "http://www.ssd.noaa.gov/PS/TROP/floaters/03E/imagery/avn-animated.gif"
    url_rgb = "http://www.ssd.noaa.gov/PS/TROP/floaters/03E/imagery/rgb-animated.gif"
    saveloc = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Blas"
    interval = timedelta(seconds=6)
    ssd.save_ssd(prepend, [url_avn, url_rgb], saveloc, interval)

if __name__ == '__main__':
    save_ssd_periodic()



