import re
from savers.common import SaveError
from util import http

__author__ = 'tangz'

from datetime import datetime as dt

DATEFORMAT = '%Y%m%d_%H%M%S'

def gettimestamp(datetime=None, frmt=DATEFORMAT):
    if datetime is None:
        datetime = dt.utcnow()
    return datetime.strftime(frmt)

def buildfilename(base=None, prependval=None, appendval=None, joiner='_'):
    parts = []
    if prependval is not None:
        parts.append(prependval)
    if base is not None:
        parts.append(base)
    if appendval is not None:
        parts.append(appendval)
    return None if not parts else joiner.join(parts)

def withdotsep(extstr):
    return extstr if extstr.startswith('.') else '.' + extstr

def withslash(folder):
    return folder if folder.endswith('/') or folder.endswith('\\') else folder + '/'


class InvalidResourceError(Exception):
    pass


class URLSource(object):
    def __init__(self, url, timeextractor=None):
        self.url = url
        self.filebase = None
        self.timestamp = None
        self.ext = None
        self.host = None
        self.extractall(timeextractor)

    def extractall(self, timeextractor):
        def checkparts(parts):
            if not parts:
                raise InvalidResourceError("Cannot parse resource name from: " + self.url)
        urlparts = re.split('/', self.url)
        checkparts(urlparts)
        filename = urlparts[-1]
        filenameparts = re.split('\.', filename)
        checkparts(filenameparts)
        filepartslen = len(filenameparts)
        if filepartslen > 1:
            self.filebase = '.'.join(filenameparts[:filepartslen-1])
            self.ext = filenameparts[-1]
        else:
            self.filebase = filename
            self.ext = None
        self.timestamp = dt.utcnow() if timeextractor is None else timeextractor(self.url)

    def __str__(self):
        return self.url


class DynamicURLSource(URLSource):
    def __init__(self, url, timeextractor=None):
        self.host = None
        self.requesturl = url
        URLSource.__init__(self, url, timeextractor)

    def extractall(self, timeextractor):
        self._extract_host()
        self.refresh()
        URLSource.extractall(self, timeextractor)

    def _extract_host(self):
        urlparts = re.split('/', self.url)
        if len(urlparts) > 2 and 'http' in urlparts[0]:
            self.host = urlparts[2]
        else:
            self.host = urlparts[0]

    def refresh(self):
        htmlwithimg = http.gethtmlforpage(self.requesturl)
        parser = http.ImagesHTMLParser()
        parser.feed(htmlwithimg)
        allimages = parser.foundimages

        if not allimages:
            raise SaveError("Cannot find images for: " + self.requesturl)
        elif len(allimages) == 1:
            self.url = 'http://' + withslash(self.host) + allimages[0]
        else:
            raise SaveError("Found more than one image for: " + self.requesturl)


class FileTarget(object):
    def __init__(self, folder, file, ext, timestamp):
        self.folder = folder
        self.file = file
        self.ext = ext
        self.timestamp = timestamp

    def __str__(self):
        return withslash(self.folder) + self.file + withdotsep(self.ext)


class DirectoryTarget(object):
    def __init__(self, folder):
        self.folder = folder

    def get_timestamped_file(self, base, ext, mutator=None):
        thetime = dt.utcnow()
        filebase = base if mutator is None else mutator(base)
        timestampedfile = buildfilename(base=filebase, appendval=gettimestamp(datetime=thetime))
        return FileTarget(self.folder, timestampedfile, ext, timestamp=thetime)

    def copy_filename_from(self, urlsrc, mutator=None):
        thetime = dt.utcnow() if urlsrc.timestamp is None else urlsrc.timestamp
        file = urlsrc.filebase if mutator is None else mutator(urlsrc.filebase)
        return FileTarget(self.folder, file=file, ext=urlsrc.ext, timestamp=thetime)