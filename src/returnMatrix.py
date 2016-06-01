'''
Created on 27.5.2014

@author: Eero
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ReturnMatrix(object):
    '''
    classdocs
    '''


    def __init__(self, assetList):
        '''
        Constructor
        '''
        
        self.assetList = assetList
        self.backwardReturnMatrix = self.assetList.getAssetMatrix()/ self.assetList.getAssetMatrix().shift(1)
        self.backwardReturnMatrix = self.backwardReturnMatrix.fillna(method = "pad", limit = 1).dropna(axis=0)
    
    def getReturns(self):
        return self.backwardReturnMatrix

        
    def plotReturns(self, figureIndex, plottedNames=None):
        assetNames = self.assetList.getNames()
        if not(plottedNames):
            plottedNames = assetNames 
        else:
            for n in plottedNames:
                if not(n in assetNames):
                    print "Name not found in return matrix: {0}".format(n)
                    return 1
            
        plt.figure(figureIndex)
        i = 1
        for asset in plottedNames:
            plt.subplot(self.calculateVerticalSubplotIndex(len(plottedNames), i))
            plt.plot(self.backwardReturnMatrix.index, self.backwardReturnMatrix.loc[:, asset], label = asset)
            plt.ylabel('Asset returns daily')
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            i+=1
        plt.show()
    
    def calculateVerticalSubplotIndex(self, totalPlots, plotIndex):
        return totalPlots*100 + 10 + plotIndex
        
        