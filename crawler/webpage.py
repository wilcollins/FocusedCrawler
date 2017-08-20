from bs4 import BeautifulSoup,Comment
from urllib import FancyURLopener
import tempfile
from HTMLParser import HTMLParser
import utils

from fake_useragent import UserAgent
ua = UserAgent()
ua_string = ua.google

import urlparse

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class MyOpener(FancyURLopener):
    version = ua_string

class Webpage:
    def __init__(self):
        self.pageUrl = ""
        self.title = ""
        self.text = ""
        self.outgoingUrls = []

    def __init__(self,url):
        if url is not None and url is not "":
            if not url.startswith("http"):
                url = "http://" + url
            self.pageUrl = url
            self.root_url = urlparse.urljoin(url, '/').strip("/")
            self.outgoingUrls = []
            myopener = MyOpener()
            page = myopener.open(url)
            self.soup = BeautifulSoup(page, "html.parser")
            self.outgoingUrls = self.get_outgoing_urls()
            self.title = ""
            if self.soup.title:
                self.title = self.soup.title.string
            text_nodes = self.soup.findAll(text=True)
            visible_text = filter(visible, text_nodes)
            self.text = ''.join(visible_text)
            self.text = " ".join(self.text.split())
            self.text = strip_tags(self.text)
            self.tokens = utils.tokenizeDocText(self.text)
            self.tokens = ' '.join(self.tokens)
        else:
            raise Exception("Webpage URL is not valid: (" + str(url) + ")")

    def get_outgoing_urls(self):
        if self.outgoingUrls == []:
            for link in self.soup.find_all('a', href=True):
                if link.has_attr('href'):
                    url = link['href']
                    if url.startswith('/'):
                        url = self.root_url + url
                    self.outgoingUrls.append(url)
        return self.outgoingUrls

    def save_tmp(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        self.save(file.name)
        return file.name

    def save(self, path):
        with open(path, "w") as file:
            file.write(str(self.soup))

    def score(self, scorer):
        return scorer.calculate_score(self.tokens)

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True
