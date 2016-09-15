from datetime import timedelta

from core import timing, target, saver, source

__author__ = 'tangz'

_RAL_TIME_REGEX = "\d{8}_\d{6}"
_RAL_DATEFORMAT = "%Y%m%d_%H%M%S"
_RAL_TIME_EXTRACTOR = timing.regex_timeextractor(_RAL_TIME_REGEX, _RAL_DATEFORMAT)

_RAL_VALID_EXTS = ["png"]


def save_ral_historical(station, targetdir, start, end, img_interval_min=0, bg='black'):
    thesaver = getbatchsaver(station, start, end, img_interval_min, bg)
    url = "http://weather.rap.ucar.edu/radar/nws_nids/BREF1/" + station
    jobid = station + '-refl-historical'
    thesaver.submit(jobid, url, targetdir)
    thesaver.runjob(jobid)


def getbatchsaver(station, start, end, img_interval_min, bg):
    filename_filter = lambda file: bg in file
    time_filter = timing.start_end_filter(start, end)
    filename_builder = lambda file, timestamp: station + '-' + file

    srcsetting = source.batch(timeextractor=_RAL_TIME_EXTRACTOR, valid_exts=_RAL_VALID_EXTS,
                              filename_filter=filename_filter, timefilter=time_filter)
    targsetting = target.copyfilename(filename_builder)

    return saver.Session().create_context('ral', srcsetting, targsetting,
                                          min_img_interval=timedelta(minutes=img_interval_min))
