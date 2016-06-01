'''
Created on 16.4.2014

@author: Eero
'''

from asset import Asset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AssetList(object):
    '''
    classdocs
    '''


    def __init__(self, assetNames):
        '''
        Constructor
        '''
        self.assets = []
        for a in assetNames:
            self.assets.append(Asset(a))
        
        self.start, self.end = self.getDateRange()
        rows, cols = self.getDim()
        #np.ones(rows*cols).reshape(rows, cols)
        index = pd.bdate_range(self.start, self.end)
        
        self.assetMatrix = None
        for a in self.assets:
            if type(self.assetMatrix) == type(None):
                self.assetMatrix = pd.DataFrame(a.getRawData()['Adj Close'])
            else:
                self.assetMatrix = pd.concat([self.assetMatrix, pd.DataFrame(a.getRawData()['Adj Close'])], axis = 1)
        
        self.assetMatrix.columns = assetNames
        self.assetMatrixCleaned = self.assetMatrix.fillna(method = "pad", limit = 1).dropna(axis=0)
        self.assetMatrixIndexed = self.assetMatrixCleaned.divide(self.assetMatrixCleaned.ix[0])
    
    def transformRateToBond(self, assetNames, duration):
        for a in self.assets:
            if a.getName() in assetNames:
                a.transformRateToBond(duration[assetNames.index(a.getName())])
        
        

    
    
    def __iter__(self):
        return self.assets.__iter__()
    
    def getNames(self):
        return self.assetMatrix.columns
    
    def getDim(self):
        cols = len(self.assets)
        rows = None
        for a in self.assets:
            if not(rows):
                rows = a.getLength()
            elif rows > a.getLength():
                rows = a.getLength()
        
        return rows, cols
        
    def getDateRange(self):
        
        startDate = None
        endDate = None
        
        for a in self.assets:
            if not(startDate):
                startDate = a.getMinDate()
            else:
                if startDate < a.getMinDate():
                    startDate = a.getMinDate()
            
            if not(endDate):
                endDate = a.getMaxDate()
            else:
                if endDate > a.getMaxDate():
                    endDate = a.getMaxDate()    
        
        return startDate, endDate
    
    
    def getLength(self):
        return len(self.assets)
    
    def printAssetMatrix(self):
        print "starting: {0}, ending:{1}".format(self.start, self.end)
        print self.assetMatrixCleaned
        print self.assetMatrixIndexed
    
    
    def plotByNameIndexed(self, figureIndex, plottedNames=None):
        assetNames = self.assetMatrix.columns
        if not(plottedNames):
            plottedNames = assetNames 
        else:
            for n in plottedNames:
                if not(n in assetNames):
                    print "Name not found in assetlist: {0}".format(n)
                    return 1
            
        plt.figure(figureIndex)
        for asset in plottedNames:
            plt.plot(self.assetMatrixIndexed.index, self.assetMatrixIndexed.loc[:, asset], label = asset)
        plt.ylabel('Adj Close assets')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        
    def getAssetMatrix(self):
        return self.assetMatrixCleaned
    
        
