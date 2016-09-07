from core import saver, source, target
from core import timing

__author__ = 'tangz'

_GOESPROJSCI_REGEX = "\d{10}"
_GOESPROJSCI_DATEFORMAT = "%y%m%d%H%M"

_EXTS = ["tif", "jpg"]

_FILETARG_VIS_TEMPLATE = "{sattype}-{sector}-{ts}"
_FILETARG_EC_TEMPLATE = "{sattype}-{ts}"


def savegoesprojsci(sector, savelocation, start, end, every_fifteen=True):
    thesaver = getbatchsaver(sector, start, end, every_fifteen)
    url = "http://goes.gsfc.nasa.gov/goeseast/{0}/vis/".format(sector)
    thesaver.submit("-".join([sector, "vis"]), url, savelocation)
    thesaver.save()


def savegoesprojsci_ec(savelocation, start, end, every_fifteen=True, older=False):
    sector = ""
    thesaver = getbatchsaver(sector, start, end, every_fifteen, sattype="visir-ec", template=_FILETARG_EC_TEMPLATE)
    url = "http://goes.gsfc.nasa.gov/goescolor/goeseast/hurricane2/color_med/"
    if older:
        url += "older_images/"
    thesaver.submit("visir-ec", url, savelocation)
    thesaver.save()


def getbatchsaver(sector, start, end, every_fifteen, sattype='vis', template=_FILETARG_VIS_TEMPLATE):
    removelatest = lambda file: 'latest' not in file
    timeextractor_fn = timing.regex_timeextractor(_GOESPROJSCI_REGEX, _GOESPROJSCI_DATEFORMAT)

    def timestamp_filter(timestamp):
        if not timing.start_end_filter(start, end)(timestamp):
            return False
        elif not every_fifteen:
            return True
        else:
            return timestamp.minute % 15 == 0
        # hack, 00:37 is accepted, but for all others, only save :00, :15, :30, :45.. todo: implement
        # return timestamp.minute % 15 == 0 or (timestamp.hour == 0 and timestamp.minute == 37)

    def customfilename(template, timestamp, sector, sattype):
        return template.format(sattype=sattype, sector=sector, ts=timestamp.strftime(_GOESPROJSCI_DATEFORMAT))

    srcsettg = source.batch(timeextractor=timeextractor_fn, timefilter=timestamp_filter, valid_exts=_EXTS,
                            filename_filter=removelatest)
    targsettg = target.withfiletemplate(customfilename, template, sector=sector, sattype=sattype)
    return saver.Saver(srcsettg, targsettg)
