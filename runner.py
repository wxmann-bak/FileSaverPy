from datetime import datetime, timedelta
from plugins import ral, goesprojsci, ssd

__author__ = 'tangz'

def save_ral_radar():
    station = "KRLX"
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\testscript'
    start = datetime(2016, 7, 3, 5, 0)
    end = datetime(2016, 7, 3, 7, 0)
    ral.savefromral(station, saveloc, start=start, end=end, interval=timedelta(minutes=9))


def save_goesproj_vis():
    sector = 'oklahoma'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160525_KS-OK-SD-IA-MN'
    start = datetime(2016, 5, 25, 14, 0)
    end = datetime(2016, 5, 26, 2, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)


def save_ssd_periodic():
    blas = "Blas-"
    avn_blas = "http://www.ssd.noaa.gov/PS/TROP/floaters/03E/imagery/avn-animated.gif"
    rgb_blas = "http://www.ssd.noaa.gov/PS/TROP/floaters/03E/imagery/rgb-animated.gif"
    saveloc_blas = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Blas"

    nepartak = "Nepartak-"
    avn_nepartak = "http://www.ssd.noaa.gov/PS/TROP/floaters/02W/imagery/avn-animated.gif"
    rgb_nepartak = "http://www.ssd.noaa.gov/PS/TROP/floaters/02W/imagery/rgb-animated.gif"
    saveloc_nepartak = "C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Nepartak"

    interval = timedelta(seconds=10)
    ssd.save_ssd(blas, [avn_blas, rgb_blas], saveloc_blas, interval)
    ssd.save_ssd(nepartak, [avn_nepartak, rgb_nepartak], saveloc_nepartak, interval)

if __name__ == '__main__':
    save_ssd_periodic()



