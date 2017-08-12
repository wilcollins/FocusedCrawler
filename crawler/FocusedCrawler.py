#!/usr/local/bin/python
import numpy as np

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
    conf = FCConfig("config.ini")
    seedUrls = linesFromFile(conf["seedFile"])
    docDirPath = conf["docsFileDir"]
    docDirPath = os.path.abspath(docDirPath)
    repositoryDocNames = [y for x in os.walk(docDirPath) for y in glob(os.path.join(x[0], '*.html'))]

    if conf["useVSM"]:
        # use VSM model to label training docs
        vsmModel = None
        if conf["VSMFilterModel"].lower() == "tf-idf":
            vsmModel = TfidfScorer(getUrlTexts(seedUrls))
        elif conf["VSMFilterModel"].lower() == "lsi":
            vsmModel = LSIScorer(getUrlTexts(seedUrls))
        print "constructed vsm model"

        relevantDocs , irrelevantDocs = vsmModel.labelDocs(
            repositoryDocNames, conf["minRepositoryDocNum"],
            conf["filterIrrelevantThreshold"],
            conf["filterRelevantThreshold"])
    else:
        print "Using labels provided by filepath, ie. ./html_files/relevant && ./html_files/irrelevant"
        for filepath in repositoryDocNames:
            print filepath
        irrelevantDocs = [filepath for filepath in repositoryDocNames if "irrelevant" in filepath]
        relevantDocs = list(set(repositoryDocNames) - set(irrelevantDocs))
        print "Found {} relevantDocs & {} irrelevantDocs".format(len(relevantDocs), len(irrelevantDocs))

    # Train classifier
    classifier = None
    testSize = min(len(relevantDocs), len(irrelevantDocs))
    trainSize = conf["trainDocNum"]
    if (trainSize > testSize):
        raise Exception("Training size ({}) is larger than test size ({})".format(trainSize, testSize))


    trainDocs = relevantDocs[:trainSize] + irrelevantDocs[:trainSize]
    trainLabels = [1]*trainSize + [0]*trainSize
    if conf["classifier"].upper() == "NB":
        classifier = NaiveBayesClassifier()
    elif conf["classifier"].upper() == "SVM":
        classifier = SVMClassifier()
    classifier.trainClassifierFromNames(trainDocs, trainLabels)

    print "Training complete"

    # Test classifier
    testSize = min(len(relevantDocs), len(irrelevantDocs))
    testDocs = relevantDocs[:testSize] + irrelevantDocs[:testSize]
    testLabels = [1]*testSize + [0]*testSize
    predictedLabels = list(classifier.predictFromNames(testDocs))

    # Statistical analysis (recall and precision)
    allRelevant = testSize
    allIrrelevant = testSize
    predictedRelevant = predictedLabels.count(1)
    predictedIrrelevant = predictedLabels.count(0)
    correctlyRelevant = 0
    for i in range(0, testSize):
        if predictedLabels[i] == 1:
            correctlyRelevant += 1
    correctlyIrrelevant = 0
    for i in range(testSize, 2*testSize):
        if predictedLabels[i] == 0:
            correctlyIrrelevant += 1
    relevantRecall = float(correctlyRelevant) / allRelevant
    relevantPrecision = float(correctlyRelevant) / (predictedRelevant)
    irrelevantRecall = float(correctlyIrrelevant) / allIrrelevant
    irrelevantPrecision = float(correctlyIrrelevant) / (predictedIrrelevant)
    print relevantRecall, relevantPrecision


    [(-1,p) for p in seedUrls]
    priorityQueue = PriorityQueue(t)
    crawler = Crawler(priorityQueue,classifier,10)
    crawler.crawl()
    print crawler.relevantPagesCount

    print crawler.pagesCount


if __name__ == "__main__":
    x = main()
