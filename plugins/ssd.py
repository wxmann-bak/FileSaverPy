from core import source, target, saver

__author__ = 'tangz'

_DATEFORMAT = '%Y%m%d_%H%M%S'


def save_ssd_animated(storm_id, sattypes, saveloc, saveperiod, begin=None, end=None):
    mutator = lambda file, timestamp: "-".join(
        [storm_id, file.replace("-animated", ""), timestamp.strftime(_DATEFORMAT)])
    context = saver.Session().create_context(storm_id, source.singular(), target.copyfilename(mutator),
                                             saveperiod=saveperiod)
    for sattype in sattypes:
        url = "http://www.ssd.noaa.gov/PS/TROP/floaters/{0}/imagery/{1}-animated.gif".format(storm_id, sattype.lower())
        jobid = '-'.join([storm_id, sattype])
        context.submit(jobid, url, saveloc)
    context.runall(begin, end)
    return context
