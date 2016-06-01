'''
Created on 13.2.2014

@author: Eero
'''

from financeYahooData import FinanceYahooData
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class Asset(object):
    '''
    classdocs
    '''

    figureIndex = 0

    def __init__(self, name):
        '''
        params = {
            
            name = "assetName",
            price = [0.00],
            returns = [],
            variances = [],
            varianceChanges = [],
            returnPeriods = [],
            variancePeriods = [],
            varianceChangePeriods = [],    
            correlationMatrix = [][]
        }
        '''
        
        
        
        self.name = name
        self.dataSource = FinanceYahooData(self.name)
        self.rawData = self.dataSource.getData()
        self.rawDataLength = len(self.rawData)
        self.returns = []
        self.variances = []
        self.varianceChanges = []
        self.returnPeriods = []
        self.variancePeriods = []
        self.varianceChangePeriods = "data.frame"        
        self.sharpeRatio = None
    
    def transformRateToBond(self, duration):
        output = 0*self.rawData['Adj Close']
        output[0] = 1
        dateDifference = output 
        for i in range(1, len(output)) :
            pass    
    
    
    '''
ratesToBondprices <- function(inputRates, rateDuration){
    
    output <- 0*inputRates
    output[1] <- 1
    indexDifference <- as.numeric(diff(index(inputRates)))
    inputRates <- coredata(inputRates)/100
    for(i in 2:length(inputRates)){
        rate <- inputRates[i]
        oldRate <- inputRates[i-1]
        if(rate > 0){
            output[i] <- ( oldRate*(1 + rate)^(1+rateDuration) - oldRate*(1 + rate) + rate*(1 + rate) )/( rate*(1 + rate)^(1+rateDuration) ) * ( 1+rate )^(indexDifference[i-1]/365.25)
        }else{
            output[i] <- 1 + rateDuration*oldRate
        }
    }
    return(cumprod(output))
}
'''
           
    def printChart(self, index):
        plt.figure(index)
        plt.plot(self.rawData.index, self.rawData['Adj Close'])
        plt.ylabel('Adj Close of {0}'.format(self.name))
        plt.show()
    
    def printChartLog(self, index):
        plt.figure(index)
        plt.plot(self.rawData.index, np.log10(self.rawData['Adj Close']))
        plt.ylabel('Adj Close of {0}'.format(self.name))
        plt.show()
    
    def printChartComb(self, index):
        plt.figure(index)
        plt.subplot(211)
        plt.plot(self.rawData['Adj Close'])
        plt.subplot(212)
        plt.plot(self.rawData.index, np.log10(self.rawData['Adj Close']))
        plt.ylabel('Adj Close of {0}'.format(self.name))
        plt.show()       
    
    def calculateSharpe(self, cashreturns):
        self.sharpeRatio = None
        
    
    def getName(self):
        return self.name 
    
    def getLength(self):
        return self.rawDataLength
    
    def getMinDate(self):
        return min(self.rawData.index)
    
    def getMaxDate(self):
        return max(self.rawData.index)
    
    def getRawData(self):
        return self.rawData

def main():
    #assetProto = {'name' : "^GSPC"}
    name = "GOOG"
    asset = Asset(name)
    
    name2 = "VIPS"
    asset2 = Asset(name2)
    
    name3 = "DANG"
    asset3 = Asset(name3)
    
    print(type(asset.rawData))
    print(type(asset.rawData['Adj Close']))
    print(type(asset.rawData['Adj Close'][1]))
    print(type(asset.rawData.index))
    
    
    d = pd.concat([asset.rawData['Adj Close'], asset2.rawData['Adj Close']], axis=1)
    d = pd.concat([d, pd.DataFrame(asset3.rawData['Adj Close'])], axis=1)
    d.columns = ["GOOG", "VIPS", "DANG"]
    print(type(d))
    
    
    dCleaned = d.fillna(method = "pad").dropna(axis=0)
    
    print dCleaned
    #print len(dCleaned)
    #print len(dCleaned.columns)
    #print dCleaned.ix[0]
    
    returns = dCleaned / dCleaned.shift(5)
    returns = returns.dropna(axis=0) 
    technicalSignal = returns > 1
    maxreturn = returns == returns.max(axis=1)
    #print technicalSignal
    #print maxreturn
    technicalSignal[technicalSignal == True] = 1.0
    technicalSignal[maxreturn == True] = 1.0
    technicalSignal[technicalSignal == False] = 0.0
    #print technicalSignal
    
    #print type(1.0/technicalSignal.sum(axis = 1))
    
    weights = 1.0*technicalSignal
    weights["GOOG"] = weights["GOOG"] * 1.0/technicalSignal.sum(axis = 1)
    weights["VIPS"] = weights["VIPS"] * 1.0/technicalSignal.sum(axis = 1)
    weights["DANG"] = weights["DANG"] * 1.0/technicalSignal.sum(axis = 1)
    #print technicalSignal 
    #print weights
    #print weights*returns
    #wr = weights*returns
    #print wr.sum()
    #print wr.sum(axis = 0)   
    #print (weights*returns).sum(axis = 1) 
    
    #Time deltas
    print asset.rawData.index
    print asset.rawData.index.shift()
    timeDelta = asset.rawData.index - asset.rawData.index.shift(1)
    
    
   
    
if __name__ == '__main__':
    main() 
    

'''


Asset <- setRefClass(
  "Asset",
  fields = list(
    name = "character",
    price = "ANY",
    priceLength = "numeric",
    returns = "list",
    variances = "list",
    varianceChanges = "list",
    returnPeriods = "numeric",
    variancePeriods = "numeric",
    varianceChangePeriods = "data.frame",    
    correlationMatrix = "matrix"    
  ),
  
  methods = list(
    
    setName = function(newName){
      #setter for Asset name
      name <<- newName
    },
    
    getName = function(){
      return(name)
    },
    
    setPrice = function(inputTimeSerie){
      
      if(!class(inputTimeSerie)=="zoo"){
        cat(paste("Needs input class of \"zoo\" got ", class(inputTimeSerie), "\n"))
        return            
      }
      price <<- inputTimeSerie
      priceLength <<- length(price)      
    },
    
    calculateReturn = function(period){
      if(length(which(returnPeriods == period)) == 0){
        returns[[length(returns) + 1]] <<- exp(diff(log(price), period))
        returnPeriods <<- c(returnPeriods, period)
      }      
    },
    
    calculateVariance = function(period){
      if(length(which(variancePeriods == period)) == 0){
        returnVector <- diff(log(price))
        if(period>0){
          varianceVector <- 0*price[(period+1):priceLength]
          
          for(i in 1:length(varianceVector)){
            #cat(paste("i:", i, " (i-period),(i-1):", (period+1) , (i-1), "\n"))
            varianceVector[i] <- var(returnVector[(i):(i+period-1)])
          }
        }else{
          varianceVector <- 0*price[1:(priceLength+period-1)]
          for(i in 1:length(varianceVector)){
            #cat(paste("i:", i, " (i+1),(i-period):", (i+1) , (i-period), "\n"))
            varianceVector[i] <- var(returnVector[(i+1):(i-period)])
          }
        }
        
        variances[[length(variances)+1]] <<- varianceVector
        variancePeriods <<- c(variancePeriods, period)
      }
      
    },
    
    calculateVarianceChange = function(varianceIndex, period){
      
      if(length(varianceChanges) == 0){
        varianceChanges[[length(varianceChanges) + 1]] <<- diff(variances[[varianceIndex]], period)
        varianceChangePeriods <<- data.frame(varianceIndex = varianceIndex, period = period)
      }else{
        varianceChanges[[length(varianceChanges) + 1]] <<- diff(variances[[varianceIndex]], period)
        varianceChangePeriods <<- rbind(varianceChangePeriods, c(varianceIndex, period))
      }
      
    },
    
    calculateCorrelationMatrix = function(){
      
      if(length(returns) == 0 & length(variances) == 0){
        #no need for calculations
        return
      }else if(length(returns) + length(variances) == 1 ){
        #no need for calculations
        return
      }
      
      firstName <- c()
      if(length(returns) > 0){
        for(i in 1:length(returns)){
          if(i == 1){
            correlationData <- returns[[i]]
            firstName <- paste(returnPeriods[i], "return") 
          }else{
            correlationData <- merge(correlationData, returns[[i]], all = FALSE)
            names(correlationData)[i] <- paste(returnPeriods[i], "return")
          }
        }
      }
      
      if(length(variances) > 0){
        for(i in 1:length(variances)){
          if(i == 1 & length(returns) == 0){
            correlationData <- variances[[i]]
            firstName <- paste(variancePeriods[i], "variance")
          }else{
            correlationData <- merge(correlationData, variances[[i]], all = FALSE)
            names(correlationData)[i+length(returns)] <- paste(variancePeriods[i], "variance")
          }
        }
      }
      
      if(length(varianceChanges) > 0){
        for(i in 1:length(varianceChanges)){
          correlationData <- merge(correlationData, varianceChanges[[i]], all = FALSE)
          names(correlationData)[i+length(returns)+length(variances)] <- paste(variancePeriods[varianceChangePeriods[i, 1]], "var chg", varianceChangePeriods[i, 2])
        }
      }
      
      names(correlationData)[1] <- firstName
      
      #Windsoring the data
      stds <- sapply(correlationData, sd)
      means <- colMeans(correlationData)
      for(i in 1:length(stds)){
        
        correlationData[which(correlationData[, i]-means[i] < -4*sd(correlationData[, i])), i] <- -4*sd(correlationData[, i])
        correlationData[which(correlationData[, i]-means[i] > 4*sd(correlationData[, i])), i] <- 4*sd(correlationData[, i])
        
      }
      
      correlationMatrix <<- cor(correlationData)
      
    },
    
    getReturn = function(period)
    {
      returnIndex <- which(returnPeriods == period)
      if(length(returnIndex) == 0)
      {
        # no return of period found
        return
      }
      
      return(returns[[returnIndex[1]]])
      
    },
    
    getVariance = function(period)
    {
      varianceIndex <- which(variancePeriods == period)
      cat(paste("\tvarianceIndex:", varianceIndex, "\n"))
      if(length(varianceIndex) == 0)
      {
        # no return of period found
        return
      }
      
      return(variances[[varianceIndex[1]]])
      
    },
    
    getVarianceChange = function(index, period)
    {
      varianceChangeIndex <- which(varianceChangePeriods$varianceIndex == index & varianceChangePeriods$period == period)
      cat(paste("\tvarianceChangeIndex:", varianceChangeIndex, "\n"))
      if(length(varianceChangeIndex) == 0)
      {
        # no return of period found
        return
      }
      
      return(varianceChanges[[varianceChangeIndex[1]]])
      
    },
    
    getPrice = function()
    {
      return(price)
    },
    
    plotReturns = function(){
      for(i in 1:length(returns)){
        plot(
          returns[[i]], 
          main = paste("Rolling ", returnPeriods[i], " day return of ", name)
        )
      }
    },
    
    plotVariances = function(){
      for(i in 1:length(variances)){
        plot(
          variances[[i]], 
          main = paste("Rolling ", variancePeriods[i], " day variance of ", name)
        )
      }
    },
    
    plotVarianceChanges = function(){
      for(i in 1:length(varianceChanges)){
        plot(
          varianceChanges[[i]], 
          main = paste(
            "Rolling ", 
            variancePeriods[varianceChangePeriods[i, 1]], 
            " day variance change of ", 
            varianceChangePeriods[i, 2], 
            " days ", 
            name, 
            sep="")
        )
      }
    }
    
  )
)
'''
                