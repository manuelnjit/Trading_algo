from pandas_datareader import data
from datetime import date, timedelta
from datetime import datetime
import numpy as np
import json
from statsmodels.sandbox.stats.runs import runstest_1samp
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from multiprocessing import Process, Value, Array, Pool
import multiprocessing

pennys = json.loads(open('penny_stocks.json').read()) 
            
snp = json.loads(open('snp_500.json').read())
high_vol = json.loads(open('high_vol.json').read())
single = ['SPY']
                                                      
class grab:
    def __init__(self, stock, period):
        self.stock = stock
        self.period = period

        def pan_dataread(stock, period):
            self.data = data.DataReader(stock, data_source='yahoo',
                                        start=date.today() - timedelta(days=int(period)),
                                        end=date.today().strftime("%Y-%m-%d"))['Adj Close'].pct_change().dropna()
    
        pan_dataread(self.stock, self.period)
        

portfolio = high_vol

def forecast_chart(obj1_, obj2_, _lag_true):
    plt.figure()
    plt.plot(obj1_.data.values, marker = 'o', linestyle = '--', color='orange')
    plt.plot(obj2_.data[_lag_true:_lag_true+len(obj1_.data)+2].values, marker = 'o', linestyle = '--', color = 'blue')
    plt.axhline(y=0)
    plt.title((str(obj1_.stock) + " vs. " + str(obj2_.stock)))

def processing_fn(datapoints):
    for stock in single:
        obj_ = grab(str(stock), 15)
        expected_returns = []
        ult_mse = []
        start = datetime.now()
        for value in portfolio:
            try:
                
                dummy_ = grab(str(value), datapoints)
            except Exception as e:
                print("There was an issue processing symbol %s with error %s" % (dummy_.stock, e))
                return
            print("Currently comparing %s with %s" % (obj_.stock, dummy_.stock))
            _correlation = []
            _lag = []
            
            for i in range(len(dummy_.data)-len(obj_.data)):
                _correlation.append(np.corrcoef(obj_.data, dummy_.data[i:i+len(obj_.data)])[0][1])
                _lag.append(i)
            
            corr_ds = pd.Series(_correlation, index = _lag)
            lag_true = corr_ds[corr_ds == corr_ds.max()].index[0]
            forecast_chart(obj_, dummy_, lag_true)
            print("max correlation", corr_ds.max(), "occurs at lag", lag_true, "with MSE: ", np.square(np.subtract(dummy_.data, obj_.data)).mean())
            ult_mse.append(np.square(np.subtract(dummy_.data, obj_.data)).mean())
            expected_returns.append(dummy_.data[lag_true+len(obj_.data)+1])
                    
        if len(_correlation) < 1:
            print('No correlations ignoring symbol %s' % value)
            return
        mse_ds = pd.Series(expected_returns, index = ult_mse)
        print("Expected Return: %s" % (sum(expected_returns)/len(expected_returns)))
        print("Max correlated Expected return: %s" % (max(expected_returns)))
        print("Max correlated Given Minimum MSE return: %s" % mse_ds[mse_ds == mse_ds.min()].index[0])
        
        p = 0
        for value in expected_returns:
            if value > 0:
                p += 1
            
        print("Probability tomorrow is positive: %s" % (p/len(expected_returns)))
        print("Computation Duration: %s " % (datetime.now() - start))


if __name__ == '__main__':
    cpu_cores = multiprocessing.cpu_count()
    with Pool(processes = cpu_cores) as pool:
        result = pool.map(processing_fn(25000), portfolio, 5)


