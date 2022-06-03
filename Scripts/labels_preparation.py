#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:04:19 2022

@author: abhaychaturvedi
"""


from AlgoTesting import BackTestingCls
import numpy as np
#tickers='WIPRO.NS'
#tickers='RELIANCE.NS'
tickers='BTC-USD'
bt=BackTestingCls(tickers, last_n_days=7, interval='1m')

target_col='trend'
target_col1='trend1'
target_col2='trend2'

# =============================================================================
# bt.movingSlopeLabel(label=target_col1, window=30, shift_=-30)
# bt.movingSlopeLabel(label=target_col2, window=80, shift_=-80)
# =============================================================================
#wipro 30, 80, //2, 0.5
s_=30
l_=80

bt.weightedMovSlopeLabel(label='trend', window_s=s_, window_l=l_, shift_s=-s_//2, shift_l=-l_//2, weight_s=0.4)

bt.get_indicators()
bt.ohlc_data.drop(["Final Lowerband", "Final Upperband"], axis=1, inplace=True)

##########################################
####### plotting prepaired labels #######
##########################################

color_dict = ['#ff0a0a', '#ff7c0a', '#ffd60a', '#c6ff0a', '#74ff0a', '#0aff33', '#0a3811']
``
bt.ohlc_data['rank']=range(len(bt.ohlc_data))

def color_selection_for_labels(x):
    if x<-0.1:
        return color_dict[0]
    elif x<0:
        return color_dict[1]
    elif x<0.1:
        return color_dict[-2]
    elif x>=0.1:
        return color_dict[-1]
    else:
        return '#000103'
        
s_=-2000
e_=-1
def plot_label( target_col, s_=-500, e_=-1):
    bt.ohlc_data[s_:e_].plot.scatter(x='rank', y="Adj Close",s=4, color = [color_selection_for_labels(x) for x in bt.ohlc_data[target_col]][s_:e_])

plot_label(target_col=target_col, s_=s_, e_=e_)

# =============================================================================
# plot_label(target_col=target_col1, s_=s_, e_=e_)
# plot_label(target_col=target_col2, s_=s_, e_=e_)
# =============================================================================

bt.ohlc_data[target_col][s_:e_].plot()


# =============================================================================
# 
# t1_=bt.ohlc_data[target_col1][s_:e_]
# t2_=bt.ohlc_data[target_col2][s_:e_]
# bt.ohlc_data.trend.plot()
# print(bt.ohlc_data.trend1.min(), bt.ohlc_data.trend1.max())
# print(bt.ohlc_data.trend2.min(), bt.ohlc_data.trend2.max())
# 
# =============================================================================
