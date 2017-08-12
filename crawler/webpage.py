from bs4 import BeautifulSoup,Comment
from urllib import FancyURLopener
import tempfile

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

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
