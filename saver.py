import files
import html.parser as hp

__author__ = 'tangz'

import urllib.request as urlreq

def dosave(srcfile, destloc):
    urlreq.urlretrieve(srcfile, destloc)


class TimeConfig(object):
    def __init__(self, interval=None, start=None, end=None):
        self.interval = interval
        if start > end:
            raise ValueError("Start time: {0} > end time: {1}".format(start, end))
        self.start = start
        self.end = end

    # def passes(self, urlsrc, hist):
    #     if self.start and self.end:
    #         rangepasses = self.start <= urlsrc.timestamp <= self.end
    #     elif self.start:
    #         rangepasses = self.start <= urlsrc.timestamp
    #     elif self.end:
    #         rangepasses = urlsrc.timestamp <= self.end
    #     else:
    #         rangepasses = True
    #
    #     if not hist:
    #         intervalpasses = True
    #     elif self.interval:
    #         dt = urlsrc.timestamp - hist[-1].timestamp
    #         intervalpasses = dt > self.interval
    #     else:
    #         intervalpasses = True
    #
    #     return rangepasses and intervalpasses


def passestime(urlsrc, timeconfig, hist):
    if not timeconfig:
        return True

    if timeconfig.start and timeconfig.end:
        rangepasses = timeconfig.start <= urlsrc.timestamp <= timeconfig.end
    elif timeconfig.start:
        rangepasses = timeconfig.start <= urlsrc.timestamp
    elif timeconfig.end:
        rangepasses = urlsrc.timestamp <= timeconfig.end
    else:
        rangepasses = True

    if not hist:
        intervalpasses = True
    elif timeconfig.interval:
        dt = urlsrc.timestamp - hist[-1].timestamp
        intervalpasses = dt > timeconfig.interval
    else:
        intervalpasses = True

    return rangepasses and intervalpasses


class BatchSaver(object):
    def __init__(self, exts=None, filter=None, timeconfig=None, timeextractor=None):
        self.hist = []
        self.exts = exts if not exts else [ext.replace('.', '') for ext in exts]
        self.filter = filter
        self.timeconfig = timeconfig
        self.timeextractor = timeextractor
        self._timeaware = self.timeextractor is not None and self.timeconfig is not None

    def _passes_outsidefilter(self, urlsrc):
        return self.filter(urlsrc) if self.filter else True

    def _passes_extfilter(self, urlsrc):
        return urlsrc.ext and self.exts and urlsrc.ext in self.exts

    # def _passes_timefilter(self, urlsrc):
    #     if not self._timeaware:
    #         return True
    #
    #     if self.timeconfig.hasstart() and self.timeconfig.hasend():
    #         return self.timeconfig.start <= urlsrc.timestamp <= self.timeconfig.end
    #     elif self.timeconfig.hasstart():
    #         return self.timeconfig.start <= urlsrc.timestamp
    #     elif self.timeconfig.hasend():
    #         return urlsrc.timestamp <= self.timeconfig.end
    #     else:
    #         return True
    #
    # def _passes_intervalfilter(self, urlsrc):
    #     if not self._timeaware:
    #         return True
    #     if not self.hist:
    #         return True
    #
    #     if self.timeconfig.hasinterval():
    #         dt = urlsrc.timestamp - self.hist[-1].timestamp
    #         return dt > self.timeconfig.interval
    #     else:
    #         return True

    def _saveone(self, url, dirtarg, mutator):
        src = files.URLSource(url, timeextractor=self.timeextractor)
        if self._passes_outsidefilter(src) and self._passes_extfilter(src) and passestime(src, self.timeconfig, self.hist):
            targloc = dirtarg.copyfrom(src, mutator)
            dosave(url, str(targloc))
            self.hist.append(targloc)
            return True
        else:
            return False

    def saveall(self, onlinedir, saveloc, mutator=None):
        allhtml = gethtmlforpage(onlinedir)
        parser = DirListingHTMLParser()
        parser.feed(allhtml)
        urls = parser.foundlinks

        dirtarg = files.DirectoryTarget(saveloc)
        for url in urls:
            self._saveone(url, dirtarg, mutator=mutator)


def gethtmlforpage(url):
    res = urlreq.urlopen(url)
    return res.read()
    # conn = http.client.HTTPConnection(url)
    # conn.putrequest('GET', "/")
    # conn.endheaders()
    # res = conn.getresponse()
    # if res.status != 200:
    #     raise HTTPResponseError("Expected 200 code, got {0} {1} instead".format(res.status, res.reason))
    # data = res.readlines()
    # res.close()
    # pagehttp = ''
    # for line in data:
    #     pagehttp += line.decode('UTF-8')
    # return pagehttp


class DirListingHTMLParser(hp.HTMLParser):
    foundlinks = []

    def handle_starttag(self, tag, attrs):
        self.foundlinks += [attrs[attr] for attr in attrs if tag == 'a' and attr == 'href']


class HTTPResponseError(Exception):
    pass


