from core import saver, source, target

__author__ = 'tangz'

_DATEFORMAT = '%Y%m%d_%H%M%S'


def save_ssd_animated(storm_id, sattypes, saveloc, saveperiod):
    mutator = lambda file, timestamp: "-".join([storm_id, file.replace("-animated", ""), timestamp.strftime(_DATEFORMAT)])
    thesaver = saver.Saver(source.singular(), target.copyfilename(mutator), saveperiod=saveperiod)
    for sattype in sattypes:
        url = "http://www.ssd.noaa.gov/PS/TROP/floaters/{0}/imagery/{1}-animated.gif".format(storm_id, sattype.lower())
        thesaver.submit("-".join([storm_id, sattype]), url, saveloc)
    thesaver.save()
