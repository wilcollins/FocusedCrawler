#!/usr/local/bin/python
import numpy as np

from crawler import Crawler
from fcconfig import FCConfig
from fcutils import linesFromFile, getUrlTexts, intLinesFromFile
from tfidfscorer import TfidfScorer
from lsiscorer import LSIScorer
from SVMClassifier import SVMClassifier
from NBClassifier import NaiveBayesClassifier
from priorityQueue import PriorityQueue

import os
from glob import glob


def main():
    fc = FocusedCrawler()
    fc.init_config()
    fc.setup_model()
    fc.train_classifier()
    fc.test_classifier()

    # Statistical analysis (recall and precision)
    fc.stat_analysis()

    fc.crawl()

class FocusedCrawler:

    def init_config(self):
        conf = FCConfig("config.ini")
        self.seedUrls = linesFromFile(conf["seedFile"])
        self.docDirPath = conf["docsFileDir"]
        self.docDirPath = os.path.abspath(self.docDirPath)
        self.repositoryDocNames = [y for x in os.walk(self.docDirPath) for y in glob(os.path.join(x[0], '*.html'))]

        self.pageLimit = conf["pageLimit"]
        self.linkLimit = conf["linkLimit"]
        self.relevantThreshold = conf["relevantThreshold"]
        self.trainSize = conf["trainDocNum"]
        self.classifierString = conf["classifier"]
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
        print "Using labels provided by filepath, ie. ./html_files/relevant && ./html_files/irrelevant"
        for filepath in self.repositoryDocNames:
            print filepath
        self.irrelevantDocs = [filepath for filepath in self.repositoryDocNames if "irrelevant" in filepath]
        self.relevantDocs = list(set(self.repositoryDocNames) - set(self.irrelevantDocs))
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
        self.classifier = None
        if (self.trainSize > self.testSize):
            raise Exception("Training size ({}) is larger than test size ({})".format(self.trainSize, self.testSize))

        trainDocs = self.relevantDocs[:self.trainSize] + self.irrelevantDocs[:self.trainSize]
        trainLabels = [1]*self.trainSize + [0]*self.trainSize
        if self.classifierString.upper() == "NB":
            self.classifier = NaiveBayesClassifier()
        elif self.classifierString.upper() == "SVM":
            self.classifier = SVMClassifier()
        self.classifier.trainClassifierFromNames(trainDocs, trainLabels)
        print "Training complete"

    def test_classifier(self):
        testDocs = self.relevantDocs[:self.testSize] + self.irrelevantDocs[:self.testSize]
        testLabels = [1]*self.testSize + [0]*self.testSize
        self.predictedLabels = list(self.classifier.predictFromNames(testDocs))

    # Statistical analysis (recall and precision)
    def stat_analysis(self):
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
            self.relevantThreshold)
        crawler.crawl()

        print crawler.relevantPages
        print len(crawler.relevantPages) / len(crawler.visited)

if __name__ == "__main__":
    x = main()
