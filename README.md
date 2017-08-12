# Focused Crawler
Originally designed as part of Virginia Tech's Crisis & Tragedy Recovery Network (CTRnet),
this project crawls the internet and collects webpages related to a given topic, often for archival purposes.

### FocusedCrawler.py
- Driver class for this project
- Responsible for creating configuration and classifier object and calling crawler

### crawler.py
-	Crawler class responsible for collecting and exploring new URLs to find relevant pages
-	Given a priority queue and a scoring class with a calculate_score(text) method

### classifier.py
-	Parent class of classifiers (non-VSM) including NaiveBayesClassifier and SVMClassifier
-	Contains code for tokenization and vectorization of document text using sklearn
-	Child classes only have to assign self.model

- #### NBClassifier.py
 - Subclass of Classifier, representing a Naïve Bayes classifier

- #### SVMClassifier.py
 -	Subclass of Classifier, representing an SVM classifier


### scorer.py
-	Parent class of scorers, which are non-classifier models, typically VSM
- #### tfidfscorer.py
  -	Subclass of Scorer, representing a tf-idf vector space model
- #### lsiscorer.py
  -	Subclass of Scorer representing an LSI vector space model

### config.ini
-	Configuration file for focused crawler in INI format

### fcconfig.py
-	Class responsible for reading configuration file, using ConfigParser
-	Adds all configuration options to its internal dictionary (e.g. config[“seedFile”])

### fcutils.py
-	Contains various utility functions relating to reading files and sanitizing/tokenizing text

### seeds.txt
-	Contains URLs to relevant pages for focused crawler to start
-	Default name, but can be modified in config.ini

### priorityQueue.py
-	Simple implementation of a priority queue using a heap

### webpage.py
- Uses BeautifulSoup and nltk to extract webpage text

### FocusedCrawlerReport.docx
For the full technical report, please visit:
https://docs.google.com/file/d/0B436PtOU57sJZkc5anMyNDZPaHM/edit?usp=sharing
