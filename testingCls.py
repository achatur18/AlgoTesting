#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 17:24:32 2022

@author: abhaychaturvedi
"""
import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

from .indicators import Indicators
from .metrics import Metrics
from .returns import Returns
from .utility import Utility
from .labelspreparation import LabelsPreparation
from .plots import Plot
from .strategy import Strategy
from .sampling import Sampling
    
class BackTestingCls(Indicators, Returns, Metrics, Utility, LabelsPreparation, Plot, Strategy, Sampling):
    def __init__(self, ticker='', last_n_days=10, interval='1d', startTime=None, endTime=None, strategy=None):
        self.ticker = ticker
        self.last_n_days = int(last_n_days)
        self.interval = interval
        self.startTime, self.endTime = self.getStartEndTime(self.last_n_days, startTime, endTime)
# =============================================================================
#         self.ohlc_data = self.get_data(self.ticker)
# =============================================================================
        self.strategy = strategy
        self.percentage_returns = 0
        
    def get_data2(self, ticker, startTime, endTime, interval):
        if (len(ticker)==0):
          print("No tickers provided!")
          return {}          
        start, end = startTime, endTime 
        # looping over tickers and creating a dataframe with close prices
        ohlc_mon = yf.download(ticker,start,end,interval=interval)
        ohlc_mon.dropna(inplace=True,how="all")    
        return ohlc_mon
    
    def get_data(self, ticker):
        if (len(ticker)==0):
          print("No tickers provided!")
          return {}          
        start, end = self.startTime, self.endTime 
        # looping over tickers and creating a dataframe with close prices
        ohlc_mon = yf.download(ticker,start,end,interval=self.interval)
        ohlc_mon.dropna(inplace=True,how="all")    
        return ohlc_mon

    

    def get_indicators(self):
        self.ohlc_data[['Supertrend', 'Final Lowerband', 'Final Upperband']] = self.Supertrend(self.ohlc_data)
        self.ohlc_data['rsi'] = self.RSI(self.ohlc_data)
        self.ohlc_data[["macd","signal", "ma_slow", "ma_fast"]] = self.MACD(self.ohlc_data)
        self.ohlc_data['ATR'] = self.ATR(self.ohlc_data)
        self.ohlc_data['ADX'] = self.ADX(self.ohlc_data)
        self.ohlc_data[["MB","UB","LB","BB_Width"]] = self.Boll_Band(self.ohlc_data)

                
    def implementStrategy(self, strategy=None):
        if strategy==None and self.strategy==None:
          strategy=self.strategy
          
        self.ohlc_data = strategy(self.ohlc_data)
        