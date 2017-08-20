#!/usr/local/bin/python
import numpy as np

from crawler import Crawler
from config import Config
from utils import linesFromFile, getUrlTexts, intLinesFromFile
from tfidfscorer import TfidfScorer
from lsiscorer import LSIScorer
from SVMClassifier import SVMClassifier
from NBClassifier import NaiveBayesClassifier
from priorityQueue import PriorityQueue
from webpage import Webpage
import google
import itertools

import os
import sys
from glob import glob

def main():
    fc = FocusedCrawler()
    fc.init_config()
    fc.setup_model()
    fc.train_classifier()

    # Statistical analysis (recall and precision)
    # fc.stat_analysis()

    fc.crawl()
    fc.cleanup_tmp_html_files()

class FocusedCrawler:

    def init_command_line_config(self):
        print "using command line argparser"
        from argparser import argdict
        conf = argdict
        self.pageLimit = conf["page_limit"]
        self.linkLimit = conf["link_limit"]
        self.relevantThreshold = conf["relevancy_threshold"]

        classifierString = conf["classifier"]
        self.classifier = None
        if "NB" in classifierString.upper():
            self.classifier = NaiveBayesClassifier()
        elif "SVM" in classifierString.upper():
            self.classifier = SVMClassifier()

        seeds = conf["seeds"]
        self.seedUrls = []
        urlsPerSeed = 10
        for keyword in seeds:
            if keyword is not None and keyword is not "":
                if "http" in keyword:
                    self.seedUrls.append(keyword)
                else:
                    seedUrlGenerator = google.search(keyword)
                    searchResultUrls = list(itertools.islice(seedUrlGenerator, 0, urlsPerSeed))
                    self.seedUrls = list(set(self.seedUrls) | set(searchResultUrls))
            else:
                raise Exception("Seed is not valid: (" + str(keyword) + ") -- it must be a keyword or URL")

        print "seed urls: "
        print self.seedUrls

        self.blacklistDomains = conf["blacklist_domains"]
        self.labeled = {}

        self.labeled["relevantUrls"] = conf["relevant_urls"]
        for url in self.labeled["relevantUrls"]:
            if url is None or url is "":
                raise Exception("Relevant URL is not valid: (" + str(url) + ")")

        self.labeled["irrelevantUrls"] = conf["relevant_urls"]
        for url in self.labeled["irrelevantUrls"]:
            if url is None or url is "":
                raise Exception("Irrelevant URL is not valid: (" + str(url) + ")")

        self.vsm = {
            "on": conf["vsm"],
            "filterModel": conf["vsm_filter"],
            "minRepositoryDocNum": conf["min_repo_doc_num"],
            "filterIrrelevantThreshold": conf["irrelevancy_threshold"],
            "filterRelevantThreshold": conf["relevancy_threshold"]
        }

    def init_config(self):
        if len(sys.argv) > 1:
            self.init_command_line_config()
        else:
            self.init_config_file_config()

    def init_config_file_config(self):
        print "using config file"
        conf = Config("config.ini")
        self.pageLimit = conf["pageLimit"]
        self.linkLimit = conf["linkLimit"]
        self.relevantThreshold = conf["relevantThreshold"]

        classifierString = conf["classifier"]
        self.classifier = None
        if "NB" in classifierString.upper():
            self.classifier = NaiveBayesClassifier()
        elif "SVM" in classifierString.upper():
            self.classifier = SVMClassifier()

        seedKeywords = linesFromFile(conf["seedFile"])
        self.seedUrls = []
        urlsPerSeed = 10
        for keyword in seedKeywords:
            if "http" in keyword:
                self.seedUrls.append(keyword)
            else:
                seedUrlGenerator = google.search(keyword)
                searchResultUrls = list(itertools.islice(seedUrlGenerator, 0, urlsPerSeed))
                self.seedUrls = list(set(self.seedUrls) | set(searchResultUrls))

        print "seed urls: "
        print self.seedUrls

        self.blacklistDomains = linesFromFile(conf["blacklistFile"])

        self.trainingDocsPath = conf["trainingDocs"]
        self.trainingDocsPath = os.path.abspath(self.trainingDocsPath)
        self.labeled = {}
        self.labeled["relevantPath"] = os.path.join(self.trainingDocsPath, "relevant.txt");
        self.labeled["irrelevantPath"] = os.path.join(self.trainingDocsPath, "irrelevant.txt");
        self.labeled["relevantUrls"] = linesFromFile(self.labeled["relevantPath"]);
        self.labeled["irrelevantUrls"] = linesFromFile(self.labeled["irrelevantPath"]);

        self.vsm = {
            "on": conf["useVSM"],
            "filterModel": conf["VSMFilterModel"],
            "minRepositoryDocNum": conf["minRepositoryDocNum"],
            "filterIrrelevantThreshold": conf["filterIrrelevantThreshold"],
            "filterRelevantThreshold": conf["filterRelevantThreshold"]
        }
        print "done"

    def setup_model(self):
        if self.vsm["on"]:
            self.setup_vsm_model()
        else:
            self.setup_labeled_model()
        self.testSize = min(len(self.relevantDocs), len(self.irrelevantDocs))

    def setup_labeled_model(self):
        print "Using labels provided by relevant.txt & irrelevant.txt"
        if self.labeled["irrelevantUrls"] is not None and len(self.labeled["irrelevantUrls"]) > 0:
            self.irrelevantDocs = [Webpage(url).save_tmp() for url in self.labeled["irrelevantUrls"] ]
        else:
            raise Exception("Irrelevant URLs must be provided for classification")
        if self.labeled["relevantUrls"] is not None and len(self.labeled["relevantUrls"]) > 0:
            self.relevantDocs = [Webpage(url).save_tmp() for url in self.labeled["relevantUrls"] ]
        else:
            raise Exception("Relevant URLs must be provided for classification")
        print "Found {} relevantDocs & {} irrelevantDocs".format(len(self.relevantDocs), len(self.irrelevantDocs))

    def setup_vsm_model(self):
        # use VSM model to label training docs
        self.vsm["model"] = None
        if self.vsmFilterModel.lower() == "tf-idf":
            self.vsm["model"] = TfidfScorer(getUrlTexts(seedUrls))
        elif self.vsmFilterModel.lower() == "lsi":
            self.vsm["model"] = LSIScorer(getUrlTexts(seedUrls))

        if self.vsm["model"] is None:
            print "No filter model specified. Cannot construct vsm model"
            sys.exit()
        else:
            print "constructed vsm model"

        self.relevantDocs , self.irrelevantDocs = self.vsm["model"].labelDocs(
            self.repositoryDocNames, self.vsm["minRepositoryDocNum"],
            self.vsm["filterIrrelevantThreshold"],
            self.vsm["filterRelevantThreshold"])

    def train_classifier(self):
        print "Training classifier"
        trainDocs = self.relevantDocs + self.irrelevantDocs
        trainLabels = [1]*len(self.relevantDocs) + [0]*len(self.irrelevantDocs)
        self.classifier.trainClassifierFromNames(trainDocs, trainLabels)
        print "Training complete"

    # Statistical analysis (recall and precision)
    def stat_analysis(self):
        testDocs = self.relevantDocs[:self.testSize] + self.irrelevantDocs[:self.testSize]
        testLabels = [1]*self.testSize + [0]*self.testSize
        self.predictedLabels = list(self.classifier.predictFromNames(testDocs))

        allRelevant = self.testSize
        allIrrelevant = self.testSize
        self.predictedRelevant = self.predictedLabels.count(1)
        self.predictedIrrelevant = self.predictedLabels.count(0)
        correctlyRelevant = 0
        for i in range(0, self.testSize):
            if self.predictedLabels[i] == 1:
                correctlyRelevant += 1
        correctlyIrrelevant = 0
        for i in range(self.testSize, 2*self.testSize):
            if self.predictedLabels[i] == 0:
                correctlyIrrelevant += 1
        self.relevantRecall = float(correctlyRelevant) / allRelevant
        self.relevantPrecision = float(correctlyRelevant) / (self.predictedRelevant)
        self.irrelevantRecall = float(correctlyIrrelevant) / allIrrelevant
        self.irrelevantPrecision = float(correctlyIrrelevant) / (self.predictedIrrelevant)
        print self.relevantRecall, self.relevantPrecision

    def crawl(self):
        t = [(-1,p) for p in self.seedUrls]
        priorityQueue = PriorityQueue(t)
        crawler = Crawler(
            priorityQueue,
            self.classifier,
            self.pageLimit,
            self.linkLimit,
            self.relevantThreshold,
            self.blacklistDomains)
        crawler.crawl()

        print crawler.relevantPages
        print len(crawler.relevantPages) / len(crawler.visited)

    def cleanup_tmp_html_files(self):
        for filepath in self.relevantDocs + self.irrelevantDocs:
            os.remove(filepath)

if __name__ == "__main__":
    x = main()
