from datetime import datetime, timedelta

from plugins import ral, goesprojsci, ssd, nasaghcc


__author__ = 'tangz'

def save_ral_radar():
    station = "KDTX"
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\Use_For_Script_testing'
    start = datetime(2016, 8, 25, 1, 0)
    end = datetime(2016, 8, 25, 1, 30)
    ral.savefromral(station, saveloc, start=start, end=end)


def save_goesproj_vis():
    sector = 'great_lakes'
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160824_IN-OH-ON-MO-KS'
    start = datetime(2016, 8, 24, 15, 0)
    end = datetime(2016, 8, 25, 1, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)


def save_ssd_periodic():
    lionrock = "Lionrock-"
    avn_lionrock = "http://www.ssd.noaa.gov/PS/TROP/floaters/12W/imagery/avn-animated.gif"
    rgb_lionrock = "http://www.ssd.noaa.gov/PS/TROP/floaters/12W/imagery/rgb-animated.gif"
    saveloc_lionrock = "C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Lionrock"

    lester = "Lester-"
    avn_lester = "http://www.ssd.noaa.gov/PS/TROP/floaters/13E/imagery/avn-animated.gif"
    rgb_lester = "http://www.ssd.noaa.gov/PS/TROP/floaters/13E/imagery/rgb-animated.gif"
    saveloc_lester = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Lester"

    madeline = 'Madeline-'
    avn_madeline = "http://www.ssd.noaa.gov/PS/TROP/floaters/14E/imagery/avn-animated.gif"
    rgb_madeline = "http://www.ssd.noaa.gov/PS/TROP/floaters/14E/imagery/rgb-animated.gif"
    saveloc_madeline = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Lester"

    gaston = 'Gaston-'
    avn_gaston = "http://www.ssd.noaa.gov/PS/TROP/floaters/07L/imagery/avn-animated.gif"
    rgb_gaston = "http://www.ssd.noaa.gov/PS/TROP/floaters/07L/imagery/rgb-animated.gif"
    saveloc_gaston = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Gaston"

    interval = timedelta(hours=5)
    # ssd.save_ssd(lionrock, [avn_lionrock, rgb_lionrock], saveloc_lionrock, interval)
    # ssd.save_ssd(lester, [avn_lester, rgb_lester], saveloc_lester, interval)
    ssd.save_ssd(madeline, [avn_madeline, rgb_madeline], saveloc_madeline, interval)
    ssd.save_ssd(gaston, [avn_gaston, rgb_gaston], saveloc_gaston, interval)


def save_nasaghcc_periodic():
    sector = nasaghcc.Sector.ATLANTIC_HURRICANE
    lat = 30.06
    long = -54.89
    sattype = nasaghcc.Satellite.INFRARED
    zoom = nasaghcc.Zoom.MEDIUM
    setting = nasaghcc.savesetting(sector, lat, long, sattype, zoom)

    nasaghcc.savenasaghcc1([setting], "C:/Users/tangz/Pictures/2016_WX/Use_For_Script_testing", save_period=timedelta(minutes=5))


if __name__ == '__main__':
    # saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\160811-15_LAFloods'
    # start = datetime(2016, 8, 9, 12, 1)
    # end = datetime(2016, 8, 15, 0, 1)
    # goesprojsci.savegoesprojsci2(saveloc, start, end)
    # save_ral_radar()
    # save_ssd_periodic()
    # save_goesproj_vis()
    save_nasaghcc_periodic()