'''
Created on 31.5.2014

@author: Eero
'''

import numpy

class MomentumFilter(object):
    '''
    classdocs
    '''


    def __init__(self, periods, weights = None, assetList = None):
        '''
        Constructor
        '''
        self.periods = periods
        if weights:
            self.weights = weights
        else:
            weights = [weights]
            self.weights = [1.0/len(periods)]*len(periods)
        self.assetList = assetList
        self.filteredAssetMatrix = None
        if self.assetList:            
            self.filteredAssetMatrix = self.calculateFilteredMatrix()
        
    
    def setAssetList(self, assetList):
        self.assetList = assetList
        self.backwardReturnMatrix = self.calculateBackwardReturnMatrix()
        self.filteredAssetMatrix = self.calculateFilteredMatrix()
    
    def updatePeriod(self, periods, weights = None):
        self.periods = periods
        if weights:
            self.weights = weights
        else:
            weights = [weights]
            self.weights = [1.0/len(periods)]*len(periods)
            
        if self.assetList:
            self.backwardReturnMatrix = self.calculateBackwardReturnMatrix()
            self.filteredAssetMatrix = self.calculateFilteredMatrix()                
    
    def calculateBackwardReturnMatrix(self):
        backwardReturnMatrix = self.assetList.getAssetMatrix()*0.0
        for i in range(0, len(self.periods)):
            if self.weights[i] > 0:
                backwardReturnMatrix = backwardReturnMatrix + self.assetList.getAssetMatrix() / self.assetList.getAssetMatrix().shift(self.periods[i]) * self.weights[i]
            else:
                backwardReturnMatrix = backwardReturnMatrix + self.assetList.getAssetMatrix().shift(self.periods[i]) / self.assetList.getAssetMatrix() * (-self.weights[i])
            backwardReturnMatrix = backwardReturnMatrix.fillna(method = "pad", limit = 1).dropna(axis=0)
                
        return backwardReturnMatrix
    
    def calculateFilteredMatrix(self):
        technicalSignal = self.backwardReturnMatrix > 1        
        maxreturn = self.backwardReturnMatrix == self.backwardReturnMatrix.max(axis=1)
        technicalSignal[technicalSignal == True] = 1.0
        technicalSignal[maxreturn == True] = 1.0
        technicalSignal[technicalSignal == False] = 0.0
        #Shifting is added to prevent lookahead bias
        return technicalSignal.shift(1)
    
    def getFilteredMatrix(self):
        return self.filteredAssetMatrix
        
    




class MomentumConfidence(MomentumFilter):
    '''
    classdocs
    '''


    def __init__(self, periods, weights = None, assetList = None):
        '''
        Constructor
        '''
        MomentumFilter.__init__(self, periods, weights, assetList)
        if self.assetList:
            self.confidenceMatrix = self.assetList.getAssetMatrix()*0.0            
            self.confidenceMatrix = self.calculateConfidenceMatrix()
        
    def setAssetList(self, assetList):
        MomentumFilter.setAssetList(self, assetList)
        if self.assetList:            
            self.confidenceMatrix = self.calculateConfidenceMatrix()
        
    def updatePeriod(self, periods, weights = None):
        MomentumFilter.updatePeriod(self, periods, weights)
        if self.assetList:
            self.confidenceMatrix = self.calculateConfidenceMatrix()             
    
    def calculateConfidenceMatrix(self):
        print "DEBUG: MomentumConfidence::calculateConfidenceMatrix"
        print self.periods
        print self.weights
        
        
        self.confidenceMatrix = self.assetList.getAssetMatrix()*0.0
        print "DEBUG: MomentumConfidence::calculateConfidenceMatrix"
        print self.confidenceMatrix
        for i in range(0, len(self.periods)):
            self.confidenceMatrix = self.confidenceMatrix + self.calculateConfidence(self.periods[i], self.weights[i])
            self.confidenceMatrix= self.confidenceMatrix.fillna(method = "pad", limit = 1).dropna(axis=0)
        #Shifting is added to prevent lookahead bias
        self.confidenceMatrix = self.confidenceMatrix.shift(1)
        print "DEBUG: MomentumConfidence::calculateConfidenceMatrix"
        print self.confidenceMatrix
    
    def calculateConfidence(self, period, weight):
        confidence = self.assetList.getAssetMatrix().shift(period)*0.0
        if weight >= 0:
            confidence = (self.assetList.getAssetMatrix().shift(period) / self.assetList.getAssetMatrix() > 1) * weight
        else:
            confidence = (self.assetList.getAssetMatrix().shift(period) / self.assetList.getAssetMatrix() < 1) * (-weight)
        
        print "DEBUG: MomentumConfidence::calculateConfidence"
        print "DEBUG: period = {0}, weight = {1}".format(period, weight)
        print self.confidenceMatrix    
        return confidence
    
    def getConfidenceMatrix(self):
        return self.confidenceMatrix
    
    def printConfidenceMatrix(self):
        print self.confidenceMatrix
        