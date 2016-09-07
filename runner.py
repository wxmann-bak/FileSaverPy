from datetime import datetime, timedelta

from plugins import ral, goesprojsci, ssd, nasaghcc


__author__ = 'tangz'

def save_ral_radar():
    station = "KDTX"
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\Use_For_Script_testing'
    start = datetime(2016, 8, 25, 1, 0)
    end = datetime(2016, 8, 25, 1, 30)
    ral.save_ral_historical(station, saveloc, start=start, end=end)


def save_goesproj_vis():
    sector = 'great_lakes'
    saveloc = '/Users/jitang/Documents/script_testing'
    start = datetime(2016, 9, 1, 18, 0)
    end = datetime(2016, 9, 2, 2, 0)
    goesprojsci.savegoesprojsci(sector, saveloc, start, end)


def save_ssd_periodic():
    lionrock = "Lionrock-"
    avn_lionrock = "http://www.ssd.noaa.gov/PS/TROP/floaters/12W/imagery/avn-animated.gif"
    rgb_lionrock = "http://www.ssd.noaa.gov/PS/TROP/floaters/12W/imagery/rgb-animated.gif"
    saveloc_lionrock = "C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Lionrock"

    lester = "13E"
    avn_lester = "http://www.ssd.noaa.gov/PS/TROP/floaters/13E/imagery/avn-animated.gif"
    rgb_lester = "http://www.ssd.noaa.gov/PS/TROP/floaters/13E/imagery/rgb-animated.gif"
    saveloc_lester = "/Users/jitang/Documents/script_testing"

    madeline = 'Madeline-'
    avn_madeline = "http://www.ssd.noaa.gov/PS/TROP/floaters/14E/imagery/avn-animated.gif"
    rgb_madeline = "http://www.ssd.noaa.gov/PS/TROP/floaters/14E/imagery/rgb-animated.gif"
    saveloc_madeline = "/Users/jitang/Documents/Lester_Script/ssd_madeline"

    gaston = 'Gaston-'
    avn_gaston = "http://www.ssd.noaa.gov/PS/TROP/floaters/07L/imagery/avn-animated.gif"
    rgb_gaston = "http://www.ssd.noaa.gov/PS/TROP/floaters/07L/imagery/rgb-animated.gif"
    saveloc_gaston = "/Users/jitang/Documents/Lester_Script/ssd_madeline"

    # interval = timedelta(seconds=10)
    # ssd.save_ssd(lionrock, [avn_lionrock, rgb_lionrock], saveloc_lionrock, interval)
    ssd.save_ssd_animated(lester, ["avn", "rgb"], saveloc_lester, timedelta(seconds=10))
    # ssd.save_ssd(madeline, [avn_madeline, rgb_madeline], saveloc_madeline, interval)
    # ssd.save_ssd(gaston, [avn_gaston, rgb_gaston], saveloc_gaston, interval)


def save_nasaghcc_all():
    epac = nasaghcc.Sector.EASTERN_PACIFIC
    atl = nasaghcc.Sector.EASTERN_NORTH_AMERICA
    # lester
    lat = 18.90#18.20#18.04#18.44 (was 18.80)
    long = -146.08#-140.00#-135.42#-130.42 (was 145.08)

    # madeline
    #lat = 19.57 #19.59 # 18.88
    #long = -149.35 #-150.25 # -145.45

    # updated_madeline
    # lat = 19.59
    # long = -150.00

    # gaston
    # lat = 32.2
    # long = -52.09

    # hermine-medium
    # lat = 28.43
    # long = -84.92

    # hermine-high

    sattype = nasaghcc.Satellite.VISIBLE
    zoom = nasaghcc.Zoom.HIGH
    maptype = nasaghcc.MapType.STANDARD
    settings = [nasaghcc.ghccsetting(epac, lat, long, sattype, zoom, past=n, maptype=maptype) for n in range(2, 18)]

    nasaghcc.savenasaghcc1(settings, "/Users/jitang/Documents/Lester_Script/lester", save_period=timedelta(hours=10))


def save_nasaghcc_periodic():
    # lester
    lat_lester = 18.80#18.20
    long_lester = -145.08#-140.00

    # hermine-medium
    lat = 28.43
    long = -84.92

    sattype = nasaghcc.Satellite.VISIBLE
    zoom = nasaghcc.Zoom.HIGH
    # maptype = nasaghcc.MapType.NONE
    lester_setting = nasaghcc.ghccsetting(nasaghcc.Sector.EASTERN_PACIFIC, lat_lester, long_lester, sattype, zoom)
    hermine_setting = nasaghcc.ghccsetting(nasaghcc.Sector.EASTERN_NORTH_AMERICA, lat, long, sattype, zoom)
    settings = [lester_setting]

    nasaghcc.savenasaghcc1(lester_setting, "/Users/jitang/Documents/script_testing", save_period=timedelta(seconds=10))

def save_ral_radar2():
    station = "KDTX"
    saveloc = '/Users/jitang/Documents/script_testing'
    start = datetime(2016, 8, 31, 1, 0)
    end = datetime(2016, 8, 31, 1, 30)
    ral.save_ral_historical(station, saveloc, start=start, end=end)


if __name__ == '__main__':
    # saveloc = '/Users/jitang/Documents/script_testing'
    # start = datetime(2016, 9, 5, 22, 1)
    # end = datetime(2016, 9, 6, 1, 1)
    # goesprojsci.savegoesprojsci_ec(saveloc, start, end)
    save_ral_radar2()
    save_ssd_periodic()
    save_goesproj_vis()
    # save_nasaghcc_all()
    save_nasaghcc_periodic()