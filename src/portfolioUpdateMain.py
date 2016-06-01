'''
Created on 27.2.2014

@author: Eero
'''

from pylab import plot, show, ylim, yticks
import matplotlib.pyplot as plt
from assetList import *
from returnMatrix import *
from allocationSystem import *
from portfolio import *
from technicalSignal import MomentumConfidence, MomentumFilter
 



def main():
    '''
    t = arange(0.0, 2.0, 0.01)
    s1 = sin(2*pi*t)
    s2 = exp(-t)
    s3 = sin(2*pi*t)*exp(-t)
    s4 = sin(2*pi*t)*cos(4*pi*t)
    
    t = arange(0.0, 2.0, 0.01)
    plot(t, s1, t, s2+1, t, s3+2, t, s4+3, color='k')
    ylim(-1,4)
    yticks(arange(4), ['S1', 'S2', 'S3', 'S4'])
    
    show()
    '''
    
    
    assetNames = ["SPY", "IEF", "SHY", "IEV", "EPP", "LQD"]
    assetList = AssetList(assetNames)
    myPort = Portfolio(assetList, "C:/Sijoitus projekti/PythonPort/TestPort")
    
    myPort.setStartingCapital(10000)
    confidenceSignal = MomentumFilter([80, 90, 100, 110, 120])
    myPort.setTechnicalSignal(confidenceSignal)
    myPort.setAllocationSystem(ConfidenceWeightSystem())
    myPort.calculatePerformance()
    myPort.printSharpe()
    myPort.printNumberOfShares()
    myPort.storePortfolioToFile()     

if __name__ == '__main__':
    main()