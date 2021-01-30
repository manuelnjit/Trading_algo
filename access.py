from pandas_datareader import data
from datetime import date, timedelta
import numpy as np
import json
from statsmodels.sandbox.stats.runs import runstest_1samp
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd

pennys = json.loads(open('penny_stocks.json').read())
# snp = json.loads(open('snp_500.json').read())
# snp2 = json.loads(open('snp_below.json').read())
snp30 = json.loads(open('snp_below30.json').read())


class penny:
    def __init__(self, stock, period):
        self.stock = stock
        self.period = period

        def pan_dataread(stock, period):

            self.data = data.DataReader(stock, data_source='yahoo',
            start = date.today()-timedelta(days=int(period)),
            end = date.today().strftime("%Y-%m-%d"))['Adj Close']

        pan_dataread(self.stock, self.period)

    def returns_plot(self):
        plt.figure()
        formatter = DateFormatter("%m/%d")
        # plt.subplot(2, 1, 1)
        # plt.plot(self.data)
        # plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

        # plt.subplot(2, 1, 2)
        plt.plot(self.data.pct_change(),marker = 'o', linestyle = '--',
                 color = 'red')
        plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
        plt.axhline(self.data.pct_change().std(), color = 'purple')
        plt.axhline(-self.data.pct_change().std(), color = 'purple')
        plt.axhline(y=0)
        plt.title((str(self.stock)+ " returns plot"))

# d = {}
# for value in snp2:
#     d[value] = penny(value, 60)
for value in pennys:
    print("currently looking at:", value)
    mfa = penny(str(value), 5000)
    sub = mfa.data[len(mfa.data)-16:len(mfa.data)-1]
    _correlations = []
    _lags = []
    for i in range(len(mfa.data)-16):
        _correlations.append(np.corrcoef(sub.pct_change().dropna(),
                                mfa.data[i:i+15].pct_change().dropna())[0][1])
        _lags.append(i)
    obj = pd.Series(_correlations, index = _lags)
    print("max correlation", obj.max(), "occurs at lag", obj[obj == obj.max()].index[0])

def graph(series1, series2):
    plt.figure()

    plt.axhline(series1.pct_change().std(), color = 'purple')
    plt.axhline(-series1.pct_change().std(), color = 'purple')
    plt.axhline(y=0)
    plt.plot(series2.pct_change().dropna().array,marker = 'o', linestyle = '--',
              color = 'orange')
    plt.plot(series1.pct_change().dropna().array,marker = 'o', linestyle = '--',
              color = 'blue')
    
    

# newlist = []
# for item in snp:
    
#     var = penny(str(item), 1)
#     if var.data.max() < 30:
#         newlist.append(var.stock)
        
# with open('snp_below30.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(newlist, ensure_ascii=False))