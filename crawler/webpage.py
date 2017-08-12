from bs4 import BeautifulSoup,Comment
from urllib import FancyURLopener
import tempfile

from fake_useragent import UserAgent
ua = UserAgent()
ua_string = ua.google

class MyOpener(FancyURLopener):
    version = ua_string

class Webpage:
    def __init__(self):
        self.pageUrl = ""
        self.title = ""
        self.text = ""

    def __init__(self,url):
        self.pageUrl = url
        myopener = MyOpener()
        page = myopener.open(url)
        self.soup = BeautifulSoup(page, "html.parser")

        self.outgoingUrls = []
        for link in self.soup.find_all('a', href=True):
            url = link['href']
            self.outgoingUrls.append(url)

        self.title = ""
        if self.soup.title:
            self.title = self.soup.title.string
        text_nodes = self.soup.findAll(text=True)
        visible_text = filter(visible, text_nodes)
        self.text = ''.join(visible_text)

    def save_tmp(self):
        file = tempfile.NamedTemporaryFile(delete=False)
        self.save(file.name)
        return file.name

    def save(self, path):
        with open(path, "w") as file:
            file.write(str(self.soup))

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    return True
