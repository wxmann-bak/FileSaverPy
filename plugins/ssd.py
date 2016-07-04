from datetime import timedelta
import threading
import saver

__author__ = 'tangz'

def save_ssd(prepend, urls, saveloc, interval):
    thesaver = saver.PeriodicSaver()
    mutator = lambda x: prepend + x.replace("-animated", "")
    for url in urls:
        thesaver.addjob(url, saveloc, interval, mutator)
    thesaver.executesaves()