
from urllib.parse import urlparse
from html.parser import HTMLParser

class URLParser(object):

    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(self.url)

    def get_domain(self):
        """
        Extracted domain from the URL (e.g berlin.de)
        """
        return self.parsed_url.netloc

    def get_prefix(self):
        """
        Basically it will return either HTTP or HTTPS
        """
        return self.parsed_url.scheme

    def get_path(self):
        """
        Return path from the URL (e.g /blog/post/die-welt/)
        """
        return self.parsed_url.path


class AnchorHTMLParser(HTMLParser):
    """
    Responsible for parsing anchor tags (<a>) and grab its attributes
    On this particular case we are interested on href attribute
    https://docs.python.org/2/library/htmlparser.html#HTMLParser.HTMLParser.handle_starttag
    """

    tag = {'name': 'a', 'attribute': 'href'}
    links = set()

    def handle_starttag(self, tag, attrs):
        if tag == self.tag['name']:
            link = dict(attrs).get(self.tag.get('attribute'))
            if link:
                self.links.add(link)

    def get_links(self):
        return self.links
