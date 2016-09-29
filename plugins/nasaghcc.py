import configparser
import re
from datetime import datetime as dt, timedelta

from core import source, urlextractors, web, target, saver


__author__ = 'tangz'

_ZOOM_MAP = {'high': 1, 'medium': 2, 'low': 4}
_REVERSE_ZOOM_MAP = {y: x for x, y in _ZOOM_MAP.items()}


def load_config(file):
    config = configparser.ConfigParser()
    config.read(file)

    mapoptions = config['MAP OPTIONS']
    positioning = config['POSITIONING']
    savesettings = config['SAVE SETTINGS']
    defaults = config['DEFAULT']

    sector = positioning['sector'].upper()
    lat = positioning.getfloat('lat')
    lon = positioning.getfloat('long')

    sattype = mapoptions['sattype'].lower()
    zoomstr = mapoptions['zoom'].lower()
    zoom = _ZOOM_MAP[zoomstr]
    maptype = mapoptions['map'].lower()

    past = defaults.getint('past')
    palette = defaults['palette']
    mapcolor = defaults['mapcolor']
    quality = defaults.getint('quality')
    width = defaults.getint('width')
    height = defaults.getint('height')

    saveloc = savesettings['dir']
    every_fifteen = savesettings.getboolean('every_fifteen_minutes')
    minutes = savesettings.getint('poll_minutes')
    saveperiod = timedelta(minutes=minutes)

    ghccset = ghccsetting(sector, lat, lon, sattype, zoom, maptype, past, palette, mapcolor, quality, width, height)
    return savenasaghcc1(ghccset, saveloc, saveperiod, every_fifteen)


def ghccsetting(sector, lat, long, sattype, zoom,
                maptype='standard', past=0, palette='ir2.pal', mapcolor='black',
                quality=90, width=1000, height=800):
    colorbar = 0  # job fails if this is = 1
    queryparams = {}
    queryparams['satellite'] = sector
    queryparams['lat'] = lat
    queryparams['lon'] = long
    queryparams['map'] = maptype
    queryparams['zoom'] = zoom
    queryparams['info'] = sattype
    queryparams['past'] = past
    if sattype != 'vis':
        queryparams['palette'] = palette
    queryparams['colorbar'] = colorbar
    queryparams['mapcolor'] = mapcolor
    queryparams['quality'] = quality
    queryparams['width'] = width
    queryparams['height'] = height
    # omitted query params: type=image, numframes={not used for image type}
    return queryparams


def tourl(ghccsettings):
    baseurl = 'http://weather.msfc.nasa.gov/cgi-bin/get-goes?'
    queryparamspart = '&'.join("{0}={1}".format(key, re.sub(r"\s+", "%20", str(ghccsettings[key]))) for key, val
                               in ghccsettings.items())
    return baseurl + queryparamspart


_TARGET_FORMAT = "ghcc-{sattype}_{ts}_[{lat},{lon}]"

_TIMESTAMP_FORMAT = "%y%m%d%H%M"


def savenasaghcc1(ghccsettings, saveloc, save_period, every_fifteen=True):
    url = tourl(ghccsettings)
    timefilter = lambda timestamp: timestamp.minute % 15 == 0 if every_fifteen else True
    src = source.singular(urlextractors.parse_html_response(web.ImagesHTMLParser), timeextractor=ghcc_timeextractor,
                          timefilter=timefilter)

    def filenamefunc(template, timestamp, sattype, lat, lon, zoom):
        return template.format(sattype=sattype, ts=timestamp.strftime(_TIMESTAMP_FORMAT), lat=lat, lon=lon, zoom=zoom)

    targ = target.withfiletemplate(filenamefunc, _TARGET_FORMAT, sattype=ghccsettings['info'], lat=ghccsettings['lat'],
                                   lon=ghccsettings['lon'], zoom=ghccsettings['zoom'])

    contextid = "_".join(
        [ghccsettings['info'], str(ghccsettings['lat']), str(ghccsettings['lon']),
         str(_REVERSE_ZOOM_MAP[ghccsettings['zoom']])])
    thecontext = saver.Context(contextid, src, targ, saveperiod=save_period)
    thecontext.submit(contextid, url, saveloc)
    return thecontext


def ghcc_timeextractor(url):
    regex = 'GOES(\d{2})(\d{2})(\d{4})(\d{1,3})'
    found = re.search(regex, url)
    if not found:
        raise url.InvalidResourceError("Cannot find date-time for file: {0}".format(url))

    found_hour = int(found.group(1))
    found_min = int(found.group(2))
    found_year = int(found.group(3))
    found_dayofyr = int(found.group(4))

    day_before_year = dt(year=found_year - 1, month=12, day=31)
    current_day = day_before_year + timedelta(days=found_dayofyr)

    return dt(year=found_year, month=current_day.month, day=current_day.day, hour=found_hour, minute=found_min)
