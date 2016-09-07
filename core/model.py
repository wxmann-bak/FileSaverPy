import os
import urllib.parse

from core.files import isfile, withdotsep


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

        self.timestamp = None if timeextractor is None else timeextractor(self.url)

    def __str__(self):
        return self.url


class FileTarget(object):
    def __init__(self, folder, file, ext, timestamp):
        self.folder = folder
        self.file = file
        self.ext = ext
        self.timestamp = timestamp

    def __str__(self):
        return os.path.join(self.folder, self.file + withdotsep(self.ext))