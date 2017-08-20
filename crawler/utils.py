import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.regexp import WordPunctTokenizer
import codecs
from string import punctuation
#from webpage import Webpage

stemmer = PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english') + list(punctuation)
tokenizer = WordPunctTokenizer()

def textsFromFilenames(fileNames):
    """ Generator function to lazily load a list of files """
    for fileName in fileNames:
        f = codecs.open(fileName, "r")
        text = f.read()
        f.close()
        yield text

def linesFromFile(fileName):
    f = codecs.open(fileName, "r")
    lines = []
    for line in f:
        lines.append(line.strip())
    f.close()
    return lines

def intLinesFromFile(fileName):
    f = codecs.open(fileName, "r")
    ints = []
    for line in f:
        ints.append(int(line.strip()))
    return ints

def getUrlTexts(urlList):
    """ Lazy returns url texts """
    # TODO: remove Webpage dependency / remove this function
    # for url in urlList:
    #     page = Webpage(url)
    #     yield page.text
    return ""

def tokenizeDocText(docText):
        """Given document text, returns list of tokens.
        These tokens are:
            - separated by whitespace/punctuation
            - not in stopword list and longer than 2
            - reduced to stem (e.g. 'computer' -> 'comput'
        """
        tokens = tokenizer.tokenize(docText)
        clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2 and not token.isdigit()]
        final = [stemmer.stem(word) for word in clean]
        return final
