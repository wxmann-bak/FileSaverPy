from savers import periodic

__author__ = 'tangz'

def save_ssd(prepend, urls, saveloc, interval):
    thesaver = periodic.PeriodicSaver()
    mutator = lambda x: prepend + x.replace("-animated", "")
    for url in urls:
        thesaver.addjob(url, saveloc, interval, mutator)
    thesaver.executesaves()