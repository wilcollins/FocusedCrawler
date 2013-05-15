import nltk
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
from nltk.tokenize.regexp import WordPunctTokenizer
#from nltk.corpus import wordnet
import re
from collections import Counter
from itertools import repeat

class Scorer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.tokenizer = WordPunctTokenizer()
        self.keywords = []
        self.score = 0

    def __init__(self,keywords):
        self.stemmer = PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.tokenizer = WordPunctTokenizer()
        self.score = 0
        keywords = ['boston','marathon','bombing', 'dzhokhar', 'tamerlan', 'tsarnaev','april', 'massachusetts', 'mit']
        self.keywords = keywords
        print(keywords)
                
    def cleanDoc(self,doc, count = 3):
        tokens = self.tokenizer.tokenize(doc)
        clean = [token.lower() for token in tokens if token.lower() not in self.stopwords and len(token) > 2 and tokens.count(token) > count]
        domains = ["guardian", "guardiannew", "cnn", "fbi", "npr", "wbur", "nytimes", "com","twitter","retweet", "via"]
        stopwords = ["said", "say", "told", "comment", "saw", "www", "http", "href", "blockquote", "other", "post"]
        clean = [dat for dat in clean if dat not in domains and dat not in stopwords and re.match("^[A-Za-z0-9]*$", dat)] #and wordnet.synsets(dat)] # and not (re.match("^[A-Za-z]+$", dat) and re.match("^[0-9]+$",dat))]
        final = [self.stemmer.stem(word) for word in clean]
        return final
    
    def normalize_list(self,L, threshold):
        cntr = Counter(L)
        least_count = cntr.most_common()[-1][1]
        if least_count > threshold:
            least_count -= 1
        cntr.subtract([item for k in cntr.keys() for item in list(repeat(k, least_count))])
        return list(cntr.elements())
        
# this function checks if the url words contain the keywords or not.
# the score given is calculated by finding how many keywords occur in the url.
    def calculate_score(self,url):
        words = url.getAllText().split('-')
        print(words)        
        for w in self.keywords:
            if w in words:
                self.score +=1
        self.score = self.score / float(len(self.keywords))
        return self.score
