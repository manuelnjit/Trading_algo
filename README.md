# Trading_algo

## Table of contents
* [About](#about)
* [Example](#example)
* [Ideas](#ideas)

## About
These scripts interact with one another to pull ipo dates of equity securities, pull data of equity securities given the ipo date and then predicts next day returns. 

## Example 
First run the new_access.py file to access ipo dates for a given json file of tickers. So for example, if you have a json file formatted as follows: 

[![Screenshot-from-2021-02-19-05-43-36.png](https://i.postimg.cc/J0TXrZMP/Screenshot-from-2021-02-19-05-43-36.png)](https://postimg.cc/n9DrTssD)

After running new_access.py you will have a new json file in the following format: 

[![Screenshot-from-2021-02-19-05-48-05.png](https://i.postimg.cc/tCKTh2SF/Screenshot-from-2021-02-19-05-48-05.png)](https://postimg.cc/mtSB4NGr)

This new format is a dictionary where the keys are the stock tickers and the values are the ipo dates. Now, we can run model1.py. Where
portfolio should be your newly formatted dictionary. Obj_ has parameters ("ticker you are interested in predicting price movements for", "time frame we are looking
at"). So if I have the number 15, I will be looking at values from 15 days ago up until today. 

After running model1.py, a dataframe is printed with the following results. 

[![Screenshot-from-2021-02-19-05-53-24.png](https://i.postimg.cc/qR2RDnNz/Screenshot-from-2021-02-19-05-53-24.png)](https://postimg.cc/XG74prcb)

The index is composed of the highest performing tickers. In this case BTU, RRD and SUP. These tickers are one standard deviation above all correlated values
to our given time series at all lags for each ticker. Lag1 is the lag at which the correlated time series begins and maxc er is the expected return of our 
security given that it will follow in the steps of our highly correlated time series. Minmse value are all values that are 1 standard deviation below all mse values
for our tickers, where mse is the minimum square error. minmse er is the expected return of our security given that it will follow in the steps of our minimum square
error time series at the given lags. 

## Ideas 
[![Screenshot-from-2021-02-19-06-57-08.png](https://i.postimg.cc/g2pXZG2v/Screenshot-from-2021-02-19-06-57-08.png)](https://postimg.cc/fJHR4nXL)
