from __future__ import division
import collections
import math
 
class Model: 
        def __init__(self, arffFile):
                self.trainingFile = arffFile
                
                #all feature names and their possible values (including the class label)
                self.features = {}

                #this is to maintain the order of features as in the arff
                self.featureNameList = []

                #contains tuples of the form (label, feature_name, feature_value)
                self.featureCounts = collections.defaultdict(lambda: 1)

                #contains all the values and the label as the last entry
                self.featureVectors = []                               

                #these will be smoothened later
                self.labelCounts = collections.defaultdict(lambda: 0)
 
        def TrainClassifier(self):
                for fv in self.featureVectors:
                        self.labelCounts[fv[len(fv)-1]] += 1 #udpate count of the label
                        for counter in range(0, len(fv)-1):
                                self.featureCounts[(fv[len(fv)-1], self.featureNameList[counter], fv[counter])] += 1
 
                for label in self.labelCounts:  #increase label counts (smoothing). remember that the last feature is actually the label
                        for feature in self.featureNameList[:len(self.featureNameList)-1]:
                                self.labelCounts[label] += len(self.features[feature])
 
        def Classify(self, featureVector):      #featureVector is a simple list like the ones that we use to train
                probabilityPerLabel = {}
                for label in self.labelCounts:
                        logProb = 0
                        for featureValue in featureVector:
                                logProb += math.log(self.featureCounts[(label, self.featureNameList[featureVector.index(featureValue)], featureValue)]/self.labelCounts[label])
                        probabilityPerLabel[label] = (self.labelCounts[label]/sum(self.labelCounts.values())) * math.exp(logProb)
                print probabilityPerLabel
                return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])
                                
        def GetValues(self):
                file = open(self.trainingFile, 'r')
                for line in file:
                        if line[0] != '@':  #start of actual data
                                self.featureVectors.append(line.strip().lower().split(','))
                        else:   #feature definitions
                                if line.strip().lower().find('@data') == -1 and (not line.lower().startswith('@relation')):
                                        self.featureNameList.append(line.strip().split()[1])
                                        self.features[self.featureNameList[len(self.featureNameList) - 1]] = line[line.find('{')+1: line.find('}')].strip().split(',')
                file.close()
 
        def TestClassifier(self, arffFile):
                file = open(arffFile, 'r')
                for line in file:
                        
                        if line[0] != '@':
                                vector = line.strip().lower().split(',')
                                print line + "classifier: " + self.Classify(vector) + " given " + vector[len(vector) - 1]
                                print "***"
		
if __name__ == "__main__":
        model = Model("tennis.arff")
        model.GetValues()
        model.TrainClassifier()
        print "*********************** Testing ***********************"
        model.TestClassifier("tennisTest.arff")
