#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 19:19:42 2022

@author: abhaychaturvedi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 16:22:16 2022

@author: abhaychaturvedi
"""

import warnings
warnings.simplefilter(action='ignore')

from AlgoTesting import LivePaperTrading, BackTestingReg
import numpy as np
import datetime as dt

#ticker='SOL-USD'
ticker='ETH-USD'
#ticker='BTC-USD'

#i=21
#start=dt.datetime.now()-dt.timedelta((i+1))
#end=dt.datetime.now()-dt.timedelta(i)

pt=BackTestingReg(ticker, last_n_days=1, interval='1m')


def superTrendStrategy(d):
    d['flag'] = "HOLD"
    temp = d['Supertrend'].shift(1)
    d['flag'][(d['Supertrend']==True) & (temp==False)] = "BUY"
    d['flag'][(d['Supertrend']==False) & (temp==True)] = "SELL"
    return d


bt=LivePaperTrading(ticker, last_n_days=1, interval='1m', strategy=superTrendStrategy)
bt.setCash(100)
import time
for i in range(len(pt.ohlc_data)//2):
    
    bt.ohlc_data = pt.ohlc_data[:len(pt.ohlc_data)//2+i]
    #bt.refreshData()
    bt.getLatestPrice()
    
    
    bt.ohlc_data["Supertrend"] = bt.Supertrend(bt.ohlc_data)['Supertrend']
    
    strategy_col='Supertrend'
    signal=bt.getSignalFromStrategy(strategy_col)
    print(signal)
    
    if signal and bt.holding==0:
        print("PERFORMING BUY!!")
        bt.buyPrice = bt.getLatestPrice()
        bt.ratioChange = bt.latestPrice/bt.buyPrice
        bt.holding = bt.ratioChange*bt.cash
        print(bt.latestPrice)
        
        print("Current Holding: ", bt.holding)
    elif ((not signal) and bt.holding>0):
        print("PERFORMING SELL!!")
        print(bt.latestPrice)
        bt.sellPrice = bt.getLatestPrice()
        bt.ratioChange = bt.latestPrice/bt.buyPrice
        bt.cash = bt.ratioChange*bt.cash
        bt.holding = 0
        
        print("Current Cash: ", bt.cash)
        
    else:
        if bt.holding>0:
            bt.sellPrice = bt.getLatestPrice()
            bt.ratioChange = bt.latestPrice/bt.buyPrice
            bt.holding = bt.ratioChange*bt.cash
            print("Current Holding: ", bt.holding)
        else:
            print("Current Cash: ", bt.cash)
    #time.sleep(6)
            
        