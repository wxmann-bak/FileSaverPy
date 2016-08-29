from html.parser import HTMLParser
import urllib.request

__author__ = 'tangz'


def gethtmlforpage(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    allhtmlbytes = res.read()
    charset = res.info().get_content_charset('iso-8859-1')
    return allhtmlbytes.decode(charset)


class LinksHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundlinks = []

    def handle_starttag(self, tag, attrs):
        self.foundlinks += [attrval for attr, attrval in attrs if tag == 'a' and attr == 'href']


class ImagesHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundimages = []

    def handle_starttag(self, tag, attrs):
        self.foundimages += [attrval for attr, attrval in attrs if tag == 'img' and attr == 'src']


class HTTPResponseError(Exception):
    pass