import os
import re
import files
import html.parser as hp
import logging

__author__ = 'tangz'

import urllib.request as urlreq

def dosave(srcfile, destloc):
    if os.path.isfile(destloc):
        raise SaveError("File: {0} already exists, cannot save it".format(destloc))
    logging.info("Saving file from {0} to {1}".format(srcfile, destloc))
    urlreq.urlretrieve(srcfile, destloc)


class TimeConfig(object):
    def __init__(self, interval=None, start=None, end=None):
        self.interval = interval
        if start > end:
            raise ValueError("Start time: {0} > end time: {1}".format(start, end))
        self.start = start
        self.end = end


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

    def _timeaware(self):
        return self.timeextractor is not None and self.timeconfig is not None

    def _passes_outsidefilter(self, urlsrc):
        return True if not self.filter else self.filter(urlsrc.filebase)

    def _passes_extfilter(self, urlsrc):
        return urlsrc.ext and self.exts and urlsrc.ext in self.exts

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
        parser = LinksHTMLParser()
        parser.feed(allhtml)
        alllinks = parser.foundlinks
        urls = [files.withslash(onlinedir) + link for link in alllinks if re.search("\.\w{3}$", link)]

        dirtarg = files.DirectoryTarget(saveloc)
        for url in urls:
            self._saveone(url, dirtarg, mutator=mutator)


def gethtmlforpage(url):
    res = urlreq.urlopen(url)
    allhtmlbytes = res.read()
    return allhtmlbytes.decode('UTF-8')


class LinksHTMLParser(hp.HTMLParser):
    foundlinks = []

    def handle_starttag(self, tag, attrs):
        self.foundlinks += [attrval for attr, attrval in attrs if tag == 'a' and attr == 'href']


class SaveError(Exception):
    pass

class HTTPResponseError(Exception):
    pass


