'''
Created on 3.6.2014

@author: Eero
'''

import os.path

class PortfolioFileHandler(object):
    '''
    classdocs
    '''

    ASSET_PRICES_FILE_NAME = "assetPrices.csv"
    NUMBER_OF_SHARES_FILE_NAME = "numberOfShares.csv"
    TRADES_FILE_NAME = "trades.csv"

    def __init__(self, fileFolder):
        '''
        Constructor
        '''
        
        if fileFolder.endswith('/'):
            pass
        else:
            fileFolder = fileFolder + '/'
        
        assetPricesFileName = fileFolder + PortfolioFileHandler.ASSET_PRICES_FILE_NAME
        numberOfSharesFileName = fileFolder + PortfolioFileHandler.NUMBER_OF_SHARES_FILE_NAME
        tradesFileName = fileFolder + PortfolioFileHandler.TRADES_FILE_NAME
        
        self.assetPricesFile = self.openFileWithExistenceTest(assetPricesFileName)
        self.numberOfSharesFile = self.openFileWithExistenceTest(numberOfSharesFileName)
        self.tradesFile = self.openFileWithExistenceTest(tradesFileName)
    
    
    def openFileWithExistenceTest(self, fileName):
        if os.path.isfile(fileName):
            return open(fileName, "r+")
        else:
            return open(fileName, "w")    
     
     
    def getTrades(self):
        pass
    
    def writeAssetPrices(self, assetPrices):
        assetPrices.to_csv(self.assetPricesFile, sep=";")
        
    def writeNumberOfShares(self, numberOfShares):
        numberOfShares.to_csv(self.numberOfSharesFile, sep=";")
                        
    def writeTrades(self, trades):
        trades.to_csv(self.tradesFile, sep=";")
    
    
            