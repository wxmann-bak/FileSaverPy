import os
import urllib
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


def withslash(folder, fwd=True):
    if folder.endswith('/') or folder.endswith('\\'):
        return folder
    else:
        return folder + ('/' if fwd else '\\')


def isfile(url):
    urlcomponents = urllib.parse.urlparse(url)
    basepath = os.path.basename(urlcomponents.path)
    splitbasepath = os.path.splitext(basepath)
    return bool(splitbasepath[1])


def isurl(potential_url):
    return bool(urllib.parse.urlparse(potential_url).scheme)


def geturl(scheme, host, path):
    return urllib.parse.urljoin(scheme + "://" + withslash(host), path)


def get_file_url(parentpath, file):
    return urllib.parse.urljoin(withslash(parentpath), file)


class URLSource(object):
    def __init__(self, url, timeextractor=None):
        self.url = url
        self.filebase = None
        self.timestamp = None
        self.ext = None
        self.host = None
        self.scheme = None
        self.extractall(timeextractor)

    def extractall(self, timeextractor):
        urlcomponents = urllib.parse.urlparse(self.url)
        self.scheme = urlcomponents.scheme
        self.host = urlcomponents.netloc
        basepath = os.path.basename(urlcomponents.path)

        if isfile(self.url):
            splitbasepath = os.path.splitext(basepath)
            self.filebase = splitbasepath[0]
            self.ext = splitbasepath[1][1:]

        self.timestamp = dt.utcnow() if timeextractor is None else timeextractor(self.url)

    def __str__(self):
        return self.url


class DynamicURLSource(URLSource):
    def __init__(self, url, timeextractor=None):
        self.requesturl = url
        self._saved_timeextractor = timeextractor
        self._extract_protocol_host()
        self.refresh()
        URLSource.__init__(self, url, timeextractor)

    def _extract_protocol_host(self):
        urlcomponents = urllib.parse.urlparse(self.requesturl)
        self.scheme = urlcomponents.scheme
        self.host = urlcomponents.netloc

    def refresh(self):
        htmlwithimg = http.gethtmlforpage(self.requesturl)
        parser = http.ImagesHTMLParser()
        parser.feed(htmlwithimg)
        allimages = parser.foundimages

        if not allimages:
            raise SaveError("Cannot find images for: " + self.requesturl)
        elif len(allimages) == 1:
            img = allimages[0]
            self.url = img if isurl(img) else geturl(self.scheme, self.host, img)
            self.extractall(timeextractor=self._saved_timeextractor)
        else:
            raise SaveError("Found more than one image for: " + self.requesturl)


class FileTarget(object):
    def __init__(self, folder, file, ext, timestamp):
        self.folder = folder
        self.file = file
        self.ext = ext
        self.timestamp = timestamp

    def __str__(self):
        return os.path.join(self.folder, self.file + withdotsep(self.ext))


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


class InvalidResourceError(Exception):
    pass