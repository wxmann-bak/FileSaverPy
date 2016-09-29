from datetime import datetime, timedelta

from plugins import ral, goesprojsci, ssd, nasaghcc, himawari


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
    meranti = "16W"
    saveloc_meranti = "C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Meranti\\stuff\\test"
    begin = datetime.now() + timedelta(seconds=5)
    end = datetime.now() + timedelta(seconds=30)
    ssd.save_ssd_animated(meranti, ['avn', 'rgb'], saveloc_meranti, timedelta(seconds=40), begin, end)


def save_ssd_periodic_orlene():
    orlene = "16E"
    saveloc_orlene = "C:\\Users\\tangz\\Pictures\\2016_WX\\Hurricane_Orlene"

    ssd.save_ssd_animated(orlene, ['avn', 'rgb'], saveloc_orlene, timedelta(hours=5))


def save_ssd_periodic_karl():
    karl = "12L"
    saveloc_karl = "C:\\Users\\tangz\\Pictures\\2016_WX\\Karl_maybe"

    ssd.save_ssd_animated(karl, ['avn', 'rgb'], saveloc_karl, timedelta(hours=5),
                          begin=datetime(year=2016, month=9, day=19, hour=12, minute=0))


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


def save_himawari_hist():
    sattype = 'ir'
    hours = [i for i in range(5)]
    saveloc = 'C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Meranti\\closeup-' + sattype
    himawari.save_target_sector_hist(sattype, hours, saveloc)


def save_himawari_realtime():
    vis = 'vis'
    saveloc_vis = 'C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Meranti\\stuff\\test'
    himawari.save_target_sector_realtime(vis, saveloc_vis)
    #
    # ir = 'ir'
    # saveloc_ir = 'C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Meranti\\closeup-' + ir
    # himawari.save_target_sector_realtime(ir, saveloc_ir)



if __name__ == '__main__':
    # saveloc = '/Users/jitang/Documents/script_testing'
    # start = datetime(2016, 9, 5, 22, 1)
    # end = datetime(2016, 9, 6, 1, 1)
    # goesprojsci.savegoesprojsci_ec(saveloc, start, end)
    # save_ral_radar2()
    # save_ssd_periodic()
    # save_ssd_periodic_karl()
    # save_goesproj_vis()
    # save_nasaghcc_all()
    # save_nasaghcc_periodic()
    # save_himawari_realtime()
    # save_himawari_hist()
    configfile = "C:\\Users\\tangz\\Pictures\\2016_WX\\Typhoon_Megi_Test\\saveconfig.ini"
    ssd_context = ssd.load_config(configfile)
    ssd_context.runall()