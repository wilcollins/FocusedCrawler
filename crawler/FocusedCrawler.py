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

import os
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

    def init_config(self):
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

        self.seedUrls = linesFromFile(conf["seedFile"])
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

    def setup_model(self):
        if self.vsm["on"]:
            self.setup_vsm_model()
        else:
            self.setup_labeled_model()
        self.testSize = min(len(self.relevantDocs), len(self.irrelevantDocs))

    def setup_labeled_model(self):
        print "Using labels provided by relevant.txt & irrelevant.txt"
        self.irrelevantDocs = [Webpage(url).save_tmp() for url in self.labeled["irrelevantUrls"] ]
        self.relevantDocs = [Webpage(url).save_tmp() for url in self.labeled["relevantUrls"] ]
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
