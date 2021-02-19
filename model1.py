import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Process, Value, Array, Pool
import multiprocessing
import access as grab


 

portfolio = json.loads(open('pennystocks_ipo.json').read())
obj_ = grab.grab("SNDL", 15)

def forecast_chart(obj1_, obj2_, _lag_true):
    plt.figure()
    plt.plot(obj1_.data.values, marker = 'o', linestyle = '--', color='orange')
    plt.plot(obj2_.data[_lag_true:_lag_true+len(obj1_.data)+2].values, 
             marker = 'o', linestyle = '--', color = 'blue')
    plt.axhline(y=0)
    plt.title((str(obj1_.stock) + " vs. " + str(obj2_.stock)))
    plt.ylabel("Returns")

def stat_calcs():
    last_df = False
    j = 0
    for key in portfolio:
        j += 1
        print("%s/%s" % (j, len(portfolio)))
        # print(key)
        try:
            dummy_ = grab.address(str(key), portfolio[str(key)])
        except Exception as e:
            print("There was an issue processing symbol %s with error %s" % (dummy_.stock, e))
            return
        # print("Currently comparing %s with %s" % (obj_.stock, dummy_.stock))
        _correlation = []
        _lag = []
        _mse = []
        for i in range(len(dummy_.data) - len(obj_.data)):
            _correlation.append(np.corrcoef(obj_.data, dummy_.data[i:i + len(obj_.data)])[0][1])
            sub_temp = np.subtract(dummy_.data[i:i+len(obj_.data)].values, obj_.data.values)
            _mse.append(np.square(sub_temp).mean())
            _lag.append(i)
        try:            
            corr_ds = pd.Series(_correlation, index = _lag)
            ult_ds = pd.Series(_mse, index = _lag)
            loc_lagmaxcorr = corr_ds[corr_ds == corr_ds.max()].index[0]
            # # current_mse =  np.square(np.subtract(dummy_.data[loc_lagmaxcorr:loc_lagmaxcorr + len(obj_.data)], obj_.data)).mean()
            loc_lagminmse = ult_ds[ult_ds == ult_ds.min()].index[0]
            # # print("max correlation", corr_ds.max(), "occurs at lag", loc_lagmaxcorr, "with MSE: ", current_mse)
            lag_dict = {key: loc_lagmaxcorr}
            lag_dict_mse = {key: loc_lagminmse}
            expect_dict = {key: dummy_.data[loc_lagmaxcorr+len(obj_.data)+1]}
            expect_dict2 = {key: dummy_.data[loc_lagmaxcorr+len(obj_.data)+1]+dummy_.data[loc_lagmaxcorr+len(obj_.data)+2]}
            expect_dict_mse = {key: dummy_.data[loc_lagminmse+len(obj_.data)+1]}
            value_dict = {key: corr_ds.max()}
            value_dict_mse = {key: ult_ds.min()}
            temp_df = pd.DataFrame({'lag1': pd.Series(lag_dict), 'maxc value': pd.Series(value_dict), 'maxc er': pd.Series(expect_dict), '2day': pd.Series(expect_dict2),
                                    'lag2': pd.Series(lag_dict_mse), 'minmse value': pd.Series(value_dict_mse), 'minmse er': pd.Series(expect_dict_mse)})
            if last_df == False:
                last_df = True
                df = temp_df
            else:
                df = pd.concat([df, temp_df])
        except Exception as e2:
            print("There was an issue %s" %e2)
    x = df[(df['maxc value']>df['maxc value'].mean() + df['maxc value'].std())]
    final_df = x[(x['minmse value']<x['minmse value'].mean() + x['minmse value'].std())]
    print(final_df)

if __name__ == '__main__':
    cpu_cores = multiprocessing.cpu_count()
    with Pool(processes = cpu_cores) as pool:
        result = pool.map(stat_calcs(), portfolio, 5)

