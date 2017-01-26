import os
import urllib.parse


def isfile(url):
    urlcomponents = urllib.parse.urlparse(url)
    basepath = os.path.basename(urlcomponents.path)
    splitbasepath = os.path.splitext(basepath)
    return bool(splitbasepath[1])