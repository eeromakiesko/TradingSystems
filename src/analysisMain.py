'''
Created on 27.2.2014

@author: Eero
'''

from pylab import plot, show, ylim, yticks
import matplotlib.pyplot as plt
from assetList import AssetList
from returnMatrix import ReturnMatrix
from allocationSystem import EqualWeightSystem
from technicalSignal import MomentumFilter
from portfolio import Portfolio




def main():
    '''
    testing developed parts
    '''    
    
    assetNames = ["SPY", "IEF", "SHY", "IEV", "EPP", "LQD"]
    
    assetList = AssetList(assetNames)
    myPort = Portfolio(assetList)
    myPort.setStartingCapital(10000)
    momentumFilter = MomentumFilter([120, 135, 150])
    myPort.setTechnicalSignal(momentumFilter)
    myPort.setAllocationSystem(EqualWeightSystem())
    
    myPort.calculatePerformance()
    #myPort.printSharpe()
    myPort.printNumberOfShares()
    #myPort.printTrades()
    
    momentumRange = range(10, 300, 5)
    momentumSharpes = [0.0] * len(momentumRange)
    momentumReturns = [0.0] * len(momentumRange)
    momentumStds = [0.0] * len(momentumRange)
    
    
    
    #Analyzing momentum system
    i=0
    for m in momentumRange:
        print "m = {0}\n".format(m)
        momentumFilter.updatePeriod([m])
        myPort.setTechnicalSignal(momentumFilter)
        myPort.updateAllocation()
        myPort.calculatePerformance()
        momentumSharpes[i] = myPort.getSharpe()
        momentumReturns[i] = myPort.getReturn()
        momentumStds[i] = myPort.getStd()
        i += 1
     
       
       
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
     