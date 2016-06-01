'''
Created on 16.4.2014

@author: Eero
'''

from asset import *
from assetList import *
from returnMatrix import ReturnMatrix
from portfolioFileHandler import *
from math import *
import pandas as pd



class Portfolio(object):
    '''
    classdocs
    '''


    def __init__(self, assetList = None, fileFolder = None):
        '''
        Constructor
        '''        
        
        
        self.assetList = assetList
        self.returnMatrix = ReturnMatrix(self.assetList)
        
        self.startingCapital = 1
        self.allocationSystem = None
        self.technicalSignal = None
        self.portfolioReturns = None
        self.portfolioValue = None
        
        self.numberOfSharesMatrix = None
        self.trades = None
        
        self.portfolioSharpeRatio = None
        self.portfolioReturnAnnual = None
        self.portfolioStdAnnual = None
        
        if not(fileFolder):    
            self.fileHandler = None
        else:
            self.fileHandler = PortfolioFileHandler(fileFolder)
            
        
    def setStartingCapital(self, startingCapital):
        self.startingCapital = 1.0*startingCapital    
    
    def setTechnicalSignal(self, technicalSignal):
        self.technicalSignal = technicalSignal
        self.technicalSignal.setAssetList(self.assetList)
        if self.allocationSystem:
            self.allocationSystem.setTechnicalSignal(self.technicalSignal)
    
    def setAllocationSystem(self, allocationSystem):
        self.allocationSystem = allocationSystem
        self.allocationSystem.setReturnMatrix(self.returnMatrix)
        if self.technicalSignal:
            self.allocationSystem.setTechnicalSignal(self.technicalSignal)
        self.doCalculations()
    
    def updateAllocation(self):
        self.allocationSystem.setReturnMatrix(self.returnMatrix)
        if self.technicalSignal:
            self.allocationSystem.setTechnicalSignal(self.technicalSignal)
        self.doCalculations()
        
    
    def doCalculations(self):
        self.allocationSystem.calculateWeights()
        self.calculatePortfolioValue()
        self.calculateNumberOfShares() 
        self.calculateTrades()
        
     
    def getSharpe(self):
        return self.portfolioSharpeRatio
    
    def getReturn(self):
        return self.portfolioReturnAnnual
    
    def getStd(self):
        return self.portfolioStdAnnual
             
        
    def plotReturns(self, figureIndex):
        plt.figure(figureIndex)
        plt.plot(self.portfolioReturns.index, self.portfolioReturns)
        plt.ylabel('Daily portfolio returns')
        plt.show()
    
    def plotValue(self, figureIndex):
        plt.figure(figureIndex)
        plt.plot(self.portfolioValue.index, self.portfolioValue)
        plt.ylabel('Daily portfolio value')
        plt.show()
        
 
    def printStats(self):
        print "starting value: {0}".format(self.portfolioValue[0])
        print "ending value: {0}".format(self.portfolioValue[-1])
        print "start time: {0}".format(self.portfolioValue.index[0])
        print "end time: {0}".format(self.portfolioValue.index[-1])
        print "total return is {0}".format(self.portfolioValue[-1] / self.portfolioValue[0])
        print "time interval is {0} days".format(self.portfolioValue.index[-1] - self.portfolioValue.index[0])
    
    def printNumberOfShares(self):
        print "Printing number of shares of assets in portfolio"
        print self.numberOfSharesMatrix
#         for i in range(0, len(self.numberOfSharesMatrix)):
#             print self.numberOfSharesMatrix[i]
    
    def printTrades(self):
        print "Printing trades done in portfolio"
        print self.trades
        
    def calculatePortfolioValue(self):
        self.portfolioReturns = (self.allocationSystem.getWeights()*self.returnMatrix.getReturns()).sum(axis = 1)
        self.portfolioReturns = self.portfolioReturns.dropna(axis=0)
        self.portfolioValue = self.startingCapital * self.portfolioReturns.cumprod()
        
    def calculateNumberOfShares(self):
        self.numberOfSharesMatrix = self.allocationSystem.getWeights().mul(self.portfolioValue, axis="rows")
        self.numberOfSharesMatrix = self.numberOfSharesMatrix / self.assetList.getAssetMatrix()
        self.numberOfSharesMatrix = self.numberOfSharesMatrix.dropna(axis=0)
    
    def calculateTrades(self):
        self.trades =  self.numberOfSharesMatrix - self.numberOfSharesMatrix.shift(1)
        self.trades.iloc[0] = self.numberOfSharesMatrix.iloc[0]
        
    def calculatePerformance(self):        
        totalReturn = self.portfolioValue[-1] / self.portfolioValue[0]
        timeInterval = self.portfolioValue.index[-1] - self.portfolioValue.index[0]
        timeIntervalYears = timeInterval.total_seconds()/(365.25*24*60*60)
        
        self.portfolioReturnAnnual = totalReturn ** (1/timeIntervalYears)
        self.portfolioStdAnnual = self.portfolioReturns.std() * sqrt(len(self.portfolioReturns) / timeIntervalYears)
        self.portfolioSharpeRatio = (self.portfolioReturnAnnual - 1)/self.portfolioStdAnnual

    def storePortfolioToFile(self):
        self.fileHandler.writeAssetPrices(self.assetList.getAssetMatrix())
        self.fileHandler.writeNumberOfShares(self.numberOfSharesMatrix)
        self.fileHandler.writeTrades(self.trades)
    
    def printSharpe(self):
        print "annualized return: {0}".format(self.portfolioReturnAnnual) 
        print "annualized std: {0}".format(self.portfolioStdAnnual)
        print "simplified sharpe avgReturn/std = {0}".format(self.portfolioSharpeRatio)

    def printAverageAllocation(self):
        print "Average allocation for assets:"
        print self.allocationSystem.getWeights().mean(axis = 0)
        
    def printAssets(self, log=True):
        i = 0
        for a in self.assetList:
            print "Plotting {0}".format(a.getName())
            i += 1
            if log:
                a.printChartLog(i)
            else:
                a.printChart(i)
    
    def printPortfolioValue(self, log=True):
        print "Plotting portfolio value."
        if log:
            plt.figure(0)
            plt.plot(self.portfolioValue.index, np.log10(self.portfolioValue))
            plt.ylabel('Portfolio value')
            plt.show()
        else:
            plt.figure(0)
            plt.plot(self.portfolioValue.index, self.portfolioValue)
            plt.ylabel('Portfolio value')
            plt.show()
            
    
        
         
        
    
    
    
    
    
    
        