import configparser
from datetime import timedelta
from core import source, target, saver

__author__ = 'tangz'

_OUTPUT_DATEFORMAT = '%Y%m%d_%H%M%S'


def load_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    props = config['SSD']

    stormid = props['StormId']
    types = props['Types'].split(',')
    hrs = props.getint('Hours')
    outputdir = props['Dir']

    saveperiod = timedelta(hours=hrs)
    return _ssd_context_animated(stormid, types, outputdir, saveperiod)


def _ssd_context_animated(storm_id, sattypes, saveloc, saveperiod):
    mutator = lambda file, timestamp: "-".join(
        [storm_id, file.replace("-animated", ""), timestamp.strftime(_OUTPUT_DATEFORMAT)])
    srcsetting = source.singular()
    targsetting = target.copyfilename(mutator)
    context = saver.Context(srcsetting, targsetting, saveperiod=saveperiod)
    for sattype in sattypes:
        url = "http://www.ssd.noaa.gov/PS/TROP/floaters/{0}/imagery/{1}-animated.gif".format(storm_id, sattype.lower())
        jobid = '-'.join([storm_id, sattype])
        context.submit(jobid, url, saveloc)
    return context
