from html.parser import HTMLParser
import urllib.request

__author__ = 'tangz'


def gethtmlforpage(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    allhtmlbytes = res.read()
    return allhtmlbytes.decode('UTF-8')


class LinksHTMLParser(HTMLParser):
    foundlinks = []

    def handle_starttag(self, tag, attrs):
        self.foundlinks += [attrval for attr, attrval in attrs if tag == 'a' and attr == 'href']


class HTTPResponseError(Exception):
    pass