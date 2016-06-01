'''
Created on 16.4.2014

@author: Eero
'''

from numpy import *

class EqualWeightSystem(object):
    '''
    Weights assets equally. Technical filter can be used
    to filter out some of the assets. Remaining
    assets are weighted equally
    '''
    
    def __init__(self):        
        self.weights = None
        self.technicalSignal = None
        self.returnMatrix = None
    
    def setReturnMatrix(self, returnMatrix):
        self.returnMatrix = returnMatrix
    
    def setTechnicalSignal(self, technicalSignal):
        self.technicalSignal = technicalSignal
        
    def calculateWeights(self):
        if self.technicalSignal:
            self.weights = self.calculateFilteredWeights() 
        else:
            self.weights = self.returnMatrix.getReturns()*0 + 1.0/len(self.returnMatrix.getReturns().columns)
    
    def calculateFilteredWeights(self):
        self.technicalSignal.calculateFilteredMatrix()
        technicalSignal = self.technicalSignal.getFilteredMatrix()
        weights = 1.0*technicalSignal
        weights = weights.mul(1.0/technicalSignal.sum(axis = 1), axis="rows")
        return weights    
     
    
    def getWeights(self):
        return self.weights
        


class ConfidenceWeightSystem():
    '''
    Confidence based system uses confidence values c: 0<=c<=1. They are calculated
    based on some confidence algorithm. After calculation the assets weights are 
    scaled to sum one.
    '''
    
    def __init__(self):        
        self.weights = None
        self.technicalSignal = None
        self.returnMatrix = None
    
    def setReturnMatrix(self, returnMatrix):
        self.returnMatrix = returnMatrix
    
    def setTechnicalSignal(self, technicalSignal):
        self.technicalSignal = technicalSignal
        
    def calculateWeights(self):
        if self.technicalSignal:
            self.weights = self.calculateCofidenceWeights() 
        else:
            print "ConfidenceWeightSystem::calculateWeights() error: no technical signal set"
    
    def calculateCofidenceWeights(self):
        self.technicalSignal.calculateConfidenceMatrix()
        confidenceMatrix = self.technicalSignal.getConfidenceMatrix()
        print "DEBUG: ConfidenceWeightSystem::calculateCofidenceWeights"
        print confidenceMatrix
        weights = 1.0*confidenceMatrix
        weights = weights.mul(1.0/confidenceMatrix.sum(axis = 1), axis="rows")
        return weights    
     
    
    def getWeights(self):
        return self.weights
                