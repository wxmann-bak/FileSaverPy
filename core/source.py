from core.logs import logger
from core.urlextractors import staticurl, listingurl


def singular(urlsrc_func=staticurl, timeextractor=None, timefilter=None,
             valid_exts=None, filename_filter=None):
    return SourceSetting(urlsrc_func, timeextractor, timefilter, valid_exts, filename_filter)


def batch(urlset_func=listingurl, urlsrc_func=staticurl, timeextractor=None, timefilter=None,
          valid_exts=None, filename_filter=None):
    indiv_setting = SourceSetting(urlsrc_func, timeextractor, timefilter, valid_exts, filename_filter)
    return BatchSourceSetting(indiv_setting, urlset_func)


# timeextractor: raw url -> time
# timefilter: time -> pass/no pass
# filename_filter: url file base -> pass/no pass
class SourceSetting(object):
    def __init__(self, urlsrc_extractor, timeextractor, timefilter, valid_exts, filename_filter):
        self.urlsrc_extractor = urlsrc_extractor
        self.timeextractor = timeextractor
        self.timefilter = timefilter
        self._urlsrc = None
        self.exts = valid_exts
        self.filename_filter = filename_filter

    def _check_if_url_saved(self):
        if not self._urlsrc:
            raise ValueError("URL input has not be set yet.")

    def forurl(self, url):
        self._urlsrc = self.urlsrc_extractor(url)
        if self.timeextractor is not None:
            try:
                self._urlsrc.timestamp = self.timeextractor(self._urlsrc.url)
            except:
                logger.error("Cannot extract timestamp from: " + url)
        return self

    def geturlsrc(self):
        self._check_if_url_saved()
        return self._urlsrc

    def shouldsave(self):
        self._check_if_url_saved()
        return self._passes_file_filter() and self._passes_ext_filter() and self._passes_time_filter()

    def isbatch(self):
        return False

    def _passes_file_filter(self):
        if not self.filename_filter:
            return True

        if not self.filename_filter(self._urlsrc.filebase):
            self._log_exclusion("file name does not pass file name filter")
            return False
        else:
            return True

    def _passes_ext_filter(self):
        if not self._urlsrc.ext:  # is not a file
            self._log_exclusion("not a file/ could not find extension to file")
            return False
        if not self.exts:  # allows all extensions
            return True

        if not self._urlsrc.ext in self.exts:
            self._log_exclusion("extension not one of: " + self.exts)
            return False
        else:
            return True

    def _passes_time_filter(self):
        if not self.timeextractor or not self._urlsrc.timestamp:
            return True

        if not self.timefilter(self._urlsrc.timestamp):
            self._log_exclusion("timestamp does not fit in timing criteria")
            return False
        else:
            return True

    def _log_exclusion(self, reason):
        logger.debug("File: {0} excluded on basis of: {1}".format(self._urlsrc.url, reason))


# filename_builder: file base + timestamp -> new file base
class BatchSourceSetting(object):
    def __init__(self, indiv_setting, urlset_extractor):
        self._internal_setting = indiv_setting
        self._urlsrcs = []
        self.urlset_extractor = urlset_extractor

    def forurl(self, parent_url):
        newurls = self.urlset_extractor(parent_url)
        for newurl in newurls:
            self._internal_setting.forurl(newurl)
            if self._internal_setting.shouldsave():
                self._urlsrcs.append(self._internal_setting.geturlsrc())
        return self

    def isbatch(self):
        return True

    def geturlsrcs(self):
        return self._urlsrcs
