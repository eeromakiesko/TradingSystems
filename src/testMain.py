'''
Created on 27.2.2014

@author: Eero
'''

from pylab import plot, show, ylim, yticks
import matplotlib.pyplot as plt
from assetList import AssetList
from returnMatrix import ReturnMatrix
from allocationSystem import EqualWeightSystem
from portfolio import Portfolio
from technicalSignal import MomentumFilter


def main():
    '''
    testing developed parts
    '''
    
    assetNames = ["SPY", "IEF", "SHY", "IEV", "EPP", "LQD"]
    assetList = AssetList(assetNames)
    myPort = Portfolio(assetList)
    
    myPort.setStartingCapital(10000)
    technicalSignal = MomentumFilter([80, 90, 100, 110, 120])
    myPort.setTechnicalSignal(technicalSignal)
    myPort.setAllocationSystem(EqualWeightSystem())
    myPort.calculatePerformance()
    myPort.printStats()
    myPort.printSharpe()
    #myPort.printNumberOfShares()
    #myPort.printTrades()
    
    #myPort.technicalSignal.printConfidenceMatrix()
    
    myPort.printPortfolioValue()
    myPort.printAssets(log = False)
    
    longMomentumRange = range(40, 300, 10)
    shortMomentumRange = [10]*len(longMomentumRange) 
    momentumSharpes = [0.0] * len(longMomentumRange)
    momentumReturns = [0.0] * len(longMomentumRange)
    momentumStds = [0.0] * len(longMomentumRange)
    
    
    
    #Analyzing momentum system
    i=0
    for m,n in zip(longMomentumRange, shortMomentumRange):
        print "period: {0}, {1}".format(m, n)
        periods = [m, n]
        weights = [1.00, 0.00]        
        technicalSignal.updatePeriod(periods, weights)
        myPort.setTechnicalSignal(technicalSignal)
        myPort.updateAllocation()
        myPort.calculatePerformance()
        momentumSharpes[i] = myPort.getSharpe()
        momentumReturns[i] = myPort.getReturn()
        momentumStds[i] = myPort.getStd()
        i += 1
        myPort.printAverageAllocation()
     
    
    
    plt.figure(1)
    plt.plot(momentumSharpes)
    plt.show()
      
    plt.figure(2)
    plt.plot(momentumReturns)
    plt.show()
              
    plt.figure(3)
    plt.plot(momentumStds)
    plt.show()
     

if __name__ == '__main__':
    main()