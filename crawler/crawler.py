from bs4 import BeautifulSoup
from webpage import Webpage

class Crawler:
    def __init__(self, priorityQueue, scorer, pageLimit, linkLimit, relevantThreshold):
        self.visited = []
        self.relevantPages=[]
        self.totalPagesCount = len(priorityQueue.queue)
        self.priorityQueue = priorityQueue
        self.scorer = scorer
        self.pageLimit = pageLimit
        self.linkLimit = linkLimit
        self.relevantThreshold = relevantThreshold

    def pageCount(self):
        return len(self.visited)

    def crawl(self):
        hitPageLimit = False
        while self.pageCount() <  self.pageLimit and not self.priorityQueue.isempty():
            url_priority_obj = self.priorityQueue.pop()
            priority = url_priority_obj[0]
            url = url_priority_obj[1]
            if url not in self.visited:
                self.visited.append(url)
                print "Crawling page #{} {}".format(self.pageCount(), url_priority_obj)

                page = Webpage(url_priority_obj[1])
                page_score = self.scorer.calculate_score(page.text)
                if (page_score > self.relevantThreshold):
                    self.relevantPages.append(url_priority_obj)
                    print "Relevant page found. Score ({}) URL ({})".format(page_score, url)
                else:
                    print "Irrelevant page found. Score ({}) URL ({})".format(page_score, url)
                linked_url_count = 0
                for linked_url in page.outgoingUrls:
                    if linked_url != None and linked_url != '':
                        if linked_url.find('?')!= -1:
                            linked_url = linked_url.split('?')[0]
                        if linked_url not in self.visited:
                            if linked_url.startswith('http:') and linked_url.find('#') == -1 and not self.exists(linked_url,self.priorityQueue.queue):
                                linked_url_count += 1
                                print "Checking link #{} {}".format(linked_url_count, linked_url)
                                linked_page = Webpage(linked_url)
                                linked_url_score = self.scorer.calculate_score(linked_page.text)
                                self.totalPagesCount +=1
                                tot_score = (page_score + linked_url_score)/2.0
                                if tot_score > self.relevantThreshold:
                                    print "Relevant link found. Score ({}) URL ({})".format(tot_score, linked_url)
                                    self.priorityQueue.push(((-1 * tot_score),linked_url))

                                if self.linkLimit > 0 and linked_url_count >= self.linkLimit:
                                    print "Done crawling page. Reached linkLimit."
                                    break

        if self.pageCount() >=  self.pageLimit:
            print "Done crawling. Reached pageLimit."
        elif self.priorityQueue.isempty():
            print "Done crawling. No more pages to crawl."



    def exists(self,url,alist):
        urlList = [v for p,v in alist]
        return url in urlList
