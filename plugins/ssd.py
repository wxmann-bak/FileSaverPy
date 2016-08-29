from savers import periodic

__author__ = 'tangz'

def save_ssd(prepend, urls, saveloc, save_period):
    thesaver = periodic.PeriodicSaver()
    mutator = lambda x: prepend + x.replace("-animated", "")
    for url in urls:
        thesaver.addjob(url, saveloc, save_period, mutator=mutator)
    thesaver.executesaves()