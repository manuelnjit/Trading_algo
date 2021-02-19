from pandas_datareader import data
from datetime import date, timedelta

                                             
class grab:
    def __init__(self, stock, period):
        self.stock = stock
        self.period = period

        def pan_dataread(stock, period):
            self.data = data.DataReader(stock, data_source='yahoo',
                                        start=date.today() - timedelta(days=int(period)),
                                        end=date.today().strftime("%Y-%m-%d"))['Adj Close'].pct_change().dropna()
            
        pan_dataread(self.stock, self.period)
        
        
class address: 
    def __init__(self, stock, ipo_date):
        self.stock = stock
        self.ipo = ipo_date

        def pan_dataread(stock, period):
            self.data = data.DataReader(stock, data_source='yahoo',
                                        start=ipo_date,
                                        end=date.today().strftime("%Y-%m-%d"))['Adj Close'].pct_change().dropna()
            
        pan_dataread(self.stock, self.ipo)

    
