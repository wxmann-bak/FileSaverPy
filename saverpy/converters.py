import os
import urllib.parse
from datetime import datetime

from saverpy import objects


class BaseConverter(object):
    def __init__(self, timeextractor=None, use_utc=True):
        self.timeextractor = timeextractor
        self.use_utc = use_utc

    def __call__(self, url):
        src = self.convert(url)
        if src is None:
            raise ConversionException("URL must be in the form of a file link: {}".format(url))
        else:
            return [src]

    def convert(self, url, custom_timestamp=None):
        if not isfile(url):
            return None
        else:
            urlcomponents = urllib.parse.urlparse(url)
            basepath = os.path.basename(urlcomponents.path)
            splitbasepath = os.path.splitext(basepath)
            filebase = splitbasepath[0]
            ext = splitbasepath[1][1:]

            return objects.source(filename=filebase,
                                  ext=ext,
                                  timestamp=self._get_timestamp(url, custom_timestamp),
                                  url=url)

    def _get_timestamp(self, url, custom_timestamp=None):
        if self.timeextractor is not None:
            return self.timeextractor(url)

        if custom_timestamp is None:
            return _get_current_time(self.use_utc)
        else:
            return custom_timestamp


class BatchConverter(BaseConverter):
    def __init__(self, to_urls_func, timeextractor=None, use_utc=True):
        super(BatchConverter, self).__init__(timeextractor, use_utc)
        self._to_urls_func = to_urls_func

    def __call__(self, url):
        urls = self._to_urls_func(url)
        return [src for src in (self.convert(url) for url in urls) if src is not None]


def isfile(url):
    urlcomponents = urllib.parse.urlparse(url)
    basepath = os.path.basename(urlcomponents.path)
    splitbasepath = os.path.splitext(basepath)
    return bool(splitbasepath[1])


# extracting out this function for testing purposes
def _get_current_time(use_utc):
    return datetime.utcnow() if use_utc else datetime.now()


class ConversionException(Exception):
    pass
