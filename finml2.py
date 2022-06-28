# -*- coding: utf-8 -*-
import yfinance as yf
import numpy as np
import numpy as np

def sinx_(x):
    return x/((1+x**2)**0.5)

from .labelspreparation import LabelsPreparation
from .indicators import Indicators
from .plots import Plot
from .testingReg import BackTestingReg

class FinML2(BackTestingReg):
    def get_data(self, ticker, startTime, endTime, interval):
        if (len(ticker)==0):
          print("No tickers provided!")
          return {}          
        start, end = startTime, endTime 
        # looping over tickers and creating a dataframe with close prices
        ohlc_mon = yf.download(ticker,start,end,interval=interval)
        ohlc_mon.dropna(inplace=True,how="all")    
        return ohlc_mon

    def get_daily_vol(self, df, col, lookback=100):
        """
        :param close: (data frame) Closing prices
        :param lookback: (int) lookback period to compute volatility
        :return: (series) of daily volatility value
        """
        print('Calculating daily volatility for dynamic thresholds')
        close=df[col]
        
        df0 = close/close.shift(1) - 1  # daily returns
        df0 = df0.ewm(span=lookback, min_periods=lookback).std()
        return df0
    
    def getTripleBarrierLabel(self, df, priceCol, volCol=None, vthres=None, targetCol="TBlabel"):
        price = df[priceCol]
        volatility = df[volCol]

        df[targetCol] = np.nan