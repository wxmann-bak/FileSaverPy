import threading
import time
from savers import common
from util import files

__author__ = 'tangz'

class PeriodicSaver(object):
    def __init__(self):
        self.jobs = []

    def addjob(self, onlineurl, saveloc, interval, mutator=None):
        dirtarg = files.DirectoryTarget(saveloc)
        urlsrc = files.URLSource(onlineurl)
        self.jobs.append(_SaveJob(interval, urlsrc, dirtarg, mutator))

    def executesaves(self):
        for job in self.jobs:
            job.start()


class _SaveJob(threading.Thread):
    def __init__(self, interval, urlsrc, dirtarg, mutator):
        threading.Thread.__init__(self)
        self.urlsrc = urlsrc
        self.dirtarg = dirtarg
        self.mutator = mutator
        self.interval = interval

    def run(self):
        while True:
            targloc = self.dirtarg.timestamped(self.urlsrc.filebase, self.urlsrc.ext, self.mutator)
            common.dosave(self.urlsrc.url, str(targloc))
            time.sleep(self.interval.seconds)