'''
Created on 13.2.2014

@author: Eero

'''

from pandas.io.data import DataReader
from datetime import datetime
        

class FinanceYahooData(object):
    '''
    classdocs
    '''


    def __init__(self, ticker):
        '''
        Constructor
        '''
        self.startDate = datetime(1950,1,21)
        self.ticker = ticker
        
        
    def getData(self):
        return DataReader(self.ticker,  "yahoo", self.startDate, datetime.today())
        
   
   
def main():
    dataSource = FinanceYahooData("^GSPC")
    #goog = dataSource.getData("GOOG")
    sp500Ind = dataSource.getData()
    print str(sp500Ind['Adj Close'])
    
      
    
    
  
if __name__ == '__main__':
    main()        