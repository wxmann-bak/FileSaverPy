import os
import urllib.parse

from core.files import isfile
from core.logs import logger
from core.urlextractors import staticurl, listingurl


def singular(urlsrc_func=staticurl, timeextractor=None, timefilter=None, valid_exts=None,
             filename_filter=None):
    srcfilter = SourceFilter(timefilter, valid_exts, filename_filter)
    srcconverter = SourceConverter(urlsrc_func, urlset_func=None, timeextractor=timeextractor)
    return SourceSetting(srcconverter, srcfilter)


def batch(urlset_func=listingurl, urlsrc_func=staticurl, timeextractor=None, timefilter=None,
          valid_exts=None, filename_filter=None):
    srcfilter = SourceFilter(timefilter, valid_exts, filename_filter)
    srcconverter = SourceConverter(urlsrc_func, urlset_func, timeextractor)
    return SourceSetting(srcconverter, srcfilter)


# timeextractor: raw url -> time
class SourceSetting(object):
    def __init__(self, src_converter, src_filter):
        self.src_converter = src_converter
        self.src_filter = src_filter

    def urlsrcs_for(self, url, filtered=True):
        all_srcs = self.src_converter.to_sources(url)
        if not filtered:
            return all_srcs
        return [src for src in all_srcs if self.src_filter.should_save(src)]


class SourceConverter(object):
    def __init__(self, urlsrc_func, urlset_func=None, timeextractor=None):
        self.urlsrc_func = urlsrc_func
        self.urlset_func = urlset_func
        self.timeextractor = timeextractor

    def to_sources(self, url):
        if self.urlset_func:
            urls_extracted = self.urlset_func(url)
            return [self._to_source_single(url_extracted) for url_extracted in urls_extracted]
        return [self._to_source_single(url)]

    def _to_source_single(self, input_url):
        urlsrc = self.urlsrc_func(input_url)
        if self.timeextractor:
            try:
                urlsrc.timestamp = self.timeextractor(urlsrc.url)
            except:
                logger.error("Cannot extract timestamp from: " + input_url)
        return urlsrc


# timefilter: time -> pass/no pass
# filename_filter: url file base -> pass/no pass
class SourceFilter(object):
    def __init__(self, timefilter=None, valid_exts=None, filename_filter=None):
        self.timefilter = timefilter
        self.exts = valid_exts
        self.filename_filter = filename_filter

    def should_save(self, urlsrc):
        return self._passes_file_filter(urlsrc) and self._passes_ext_filter(urlsrc) \
               and self._passes_time_filter(urlsrc)

    def _passes_file_filter(self, urlsrc):
        if not self.filename_filter:
            return True

        if not self.filename_filter(urlsrc.filebase):
            SourceFilter._log_exclusion(urlsrc, "file name does not pass file name filter")
            return False
        else:
            return True

    def _passes_ext_filter(self, urlsrc):
        if not urlsrc.ext:  # is not a file
            SourceFilter._log_exclusion(urlsrc, "not a file/could not find extension to file")
            return False
        if not self.exts:  # allows all extensions
            return True

        if urlsrc.ext not in self.exts:
            SourceFilter._log_exclusion(urlsrc, "extension not one of file extensions: " + ', '.join(self.exts))
            return False
        else:
            return True

    def _passes_time_filter(self, urlsrc):
        if not urlsrc.timestamp or not self.timefilter:
            return True

        if not self.timefilter(urlsrc.timestamp):
            SourceFilter._log_exclusion(urlsrc, "timestamp does not fit in timing criteria")
            return False
        else:
            return True

    @classmethod
    def _log_exclusion(cls, urlsrc, reason):
        logger.debug("File: {0} excluded on basis of: {1}".format(urlsrc.url, reason))


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