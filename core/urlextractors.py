import core.source
from core import files, web
from core.saver import SaveError

### Single URL ###


def staticurl(url):
    return core.source.URLSource(url)


def parse_html_response(htmlparser):
    def themapper(requesturl):
        theparser = htmlparser()
        htmlwithimg = web.gethtmlforpage(requesturl)
        theparser.feed(htmlwithimg)
        allimages = theparser.foundimages

        if not allimages:
            raise SaveError("Cannot find images for: " + requesturl)
        elif len(allimages) == 1:
            img = allimages[0]
            scheme = files.get_scheme(requesturl)
            host = files.get_host(requesturl)
            url = img if files.isurl(img) else files.geturl(scheme, host, img)
            return core.source.URLSource(url)
        else:
            raise SaveError("Found more than one image for: " + requesturl)
    return themapper


### Multi URL ###


def listingurl(url):
    allhtml = web.gethtmlforpage(url)
    parser = web.LinksHTMLParser()
    parser.feed(allhtml)
    alllinks = parser.foundlinks
    # listings are always to be assumed to link to complete url's
    urls = [files.get_file_url(url, link) for link in alllinks if files.isfile(link)]
    return urls
