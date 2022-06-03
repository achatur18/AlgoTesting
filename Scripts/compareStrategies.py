#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:53:08 2022

@author: abhaychaturvedi
"""



#from AlgoTesting import BackTestingReg
from AlgoTesting import Saving
import datetime as dt
import numpy as np


##########################################
####### Making the Strategy #######
##########################################

def macdStrategy2(d):
    d['flag'] = "HOLD"
    d['flag'][(d['macd']>=d['signal']) & (d['macd_prev']<d['signal_prev'])  ] = "BUY" 
    d['flag'][(d['macd']<d['signal']) & (d['macd_prev']>=d['signal_prev'])  ] = "SELL" 
    return d

def macdStrategy(d):
    d['flag'] = "HOLD"
    d['flag'][(d['macd']>=d['signal']) ] = "BUY" 
    d['flag'][(d['macd']<d['signal']) ] = "SELL" 
    return d

def superTrendStrategy(d):
    d['flag'] = "HOLD"
    temp = d['Supertrend'].shift(1)
    d['flag'][(d['Supertrend']==True) & (temp==False)] = "BUY"
    d['flag'][(d['Supertrend']==False) & (temp==True)] = "SELL"
    return d

def superTrend_RSI(d):
    d['flag'] = "HOLD"
    d['flag'][(d['Supertrend']==True) & (d['rsi_2']<=10) ] = "BUY"
    d['flag'][(d['Supertrend']==False) & (d['rsi_2']>=90) ] = "SELL"
    return d
  
def mixStMacdStrategy(d):
    d['flag'] = "HOLD"
    temp = d['Supertrend'].shift(1)
    d['flag'][(d['Supertrend']==True) & (d['macd']>=d['signal']) ] = "BUY"
    d['flag'][(d['Supertrend']==False) ] = "SELL"
    d['flag'][(d['macd']<d['signal'])  ] = "SELL"
    return d
  
def mixStRsiMacdStrategy(d):
    d['flag'] = "HOLD"
    temp = d['Supertrend'].shift(1)
    d['flag'][(d['Supertrend']==True) & (d['macd']>=d['signal'])& (d['rsi_2']<=10)  ] = "BUY"
    d['flag'][(d['Supertrend']==False) ] = "SELL"
    d['flag'][(d['macd']<d['signal'])  ] = "SELL"
    return d
  
def movingAverage(d):
    d['flag'] = "HOLD"
    d['flag'][(d['macd']>=0) ] = "BUY" 
    d['flag'][(d['macd']<0) ] = "SELL" 
    return d

def superTrend2(d):
    d['flag'] = "HOLD"
    temp = d['Supertrend_slow'].shift(1)
    d['flag'][(d['Supertrend']==True) & (d['Supertrend_slow']==True) & (temp==False)] = "BUY"
    d['flag'][(d['Supertrend']==False) | (d['Supertrend_slow']==False)] = "SELL"
    return d

#strategies = [macdStrategy, macdStrategy2, superTrendStrategy, superTrend_RSI, mixStMacdStrategy, mixStRsiMacdStrategy, movingAverage, superTrend2]
strategies = [macdStrategy, superTrendStrategy, superTrend_RSI, mixStMacdStrategy, mixStRsiMacdStrategy]

s = Saving()

totaldays=28
freq=1
candle='5m'
ticker='BTC-USD'
#ticker='RELIANCE.NS'
filename='results/{}days{}candle({}dayfreq)-{}.csv'.format(totaldays, candle, freq, ticker)

d=s.saveStrategiesCsv(strategies=strategies, candle=candle, freq=freq, totaldays=totaldays, ticker=ticker, filename=filename)
































