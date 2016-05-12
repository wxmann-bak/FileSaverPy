__author__ = 'tangz'

import urllib.request as ur

def saveone(srcfile, destloc):
    ur.urlretrieve(srcfile, destloc)



