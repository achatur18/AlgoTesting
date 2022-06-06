#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 11:46:37 2022

@author: abhaychaturvedi
"""

import warnings
warnings.simplefilter(action='ignore')

from AlgoTesting import BackTestingReg
import numpy as np
import datetime as dt

ticker='SOL-USD'
#ticker='ETH-USD'
#ticker='BTC-USD'
#i=21
#start=dt.datetime.now()-dt.timedelta((i+1))
#end=dt.datetime.now()-dt.timedelta(i)

#bt=BackTestingReg(ticker, startTime=start, endTime=end, interval='1m')

bt=BackTestingReg(ticker, last_n_days=2, interval='1m')

target_col='trend'
bt.movingLabel(label='trend', window=81, padding=4)

########################################################
######## Plotting prepared labels ########################
################################################################
color_dict = {"BUY": '#49fc03', "SELL": "#fc0303", "HOLD": '#000000'}

bt.coloured_plot(bt.ohlc_data, target_col, color_dict)

########################################################
######## Getting different indicators########################
################################################################

bt.get_indicators()
bt.ohlc_data.drop(['Final Lowerband', 'Final Upperband'], axis=1, inplace = True)
bt.ohlc_data['macd_prev']=bt.ohlc_data['macd'].shift(1)
bt.ohlc_data['signal_prev']=bt.ohlc_data['signal'].shift(1)

bt.ohlc_data['rsi_2'] = bt.RSI(bt.ohlc_data, n=2)
bt.ohlc_data['Supertrend_slow'] = bt.Supertrend(bt.ohlc_data, atr_period=20, multiplier=5)['Supertrend']
##########################################
####### Making the Strategy #######
##########################################

import numpy as np
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


##########################################
####### Implement strategy #######
##########################################
bt.drop_na()
bt.implementStrategy(strategy=superTrendStrategy)
bt.drop_na()

##########################################
####### Calculate returns #######
##########################################
flag_column='flag'
bt.drop_na()
bt.ohlc_data[flag_column] = bt.ohlc_data[flag_column].shift(1)
bt.ohlc_data.fillna(0, inplace=True)

bt.calculateTradeReturns(flag_column=flag_column, output_column='return_flag')
print("Returns on strategy: ", bt.percentage_returns)

# Doing return claculation on whole data just to verify the calculateReturns function's 
bt.calculateTradeReturns(flag_column='trend', output_column='return_trend')
print("Returns on prepaired labels: ", bt.percentage_returns)

print("Maximum Return on one-time investment i.e. max draw up: ", bt.calculateInvestmentReturns(df_dic=None, type="max_du"))
print("Return on one-time investment", bt.calculateInvestmentReturns(df_dic=None, type="complete"))

print("Accuracy of bids on strategy", bt.calculateAccuracy("return_flag"))
print("Accuracy of bids on prepaired labels", bt.calculateAccuracy("return_trend"))
 
##########################################
####### Plot returns #######
##########################################

color_dict = {"BUY": '#49fc03', "SELL": "#fc0303", "HOLD": '#f7f7f7'}

bt.coloured_plot(bt.ohlc_data, "flag", color_dict, 0, 1000, signal_size=20)

##########################################
####### compare strategies #######
##########################################
strategies = [macdStrategy, macdStrategy2, superTrendStrategy, superTrend_RSI, mixStMacdStrategy, mixStRsiMacdStrategy, movingAverage, superTrend2]
# bt.compareStrategies(strategies)
