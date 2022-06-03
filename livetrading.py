# -*- coding: utf-8 -*-

from .testingReg import BackTestingReg


class LivePaperTrading(BackTestingReg):
    def __init__(self, ticker='', last_n_days=1, interval='1m', startTime=None, endTime=None, strategy=None):
        self.ticker = ticker
        self.last_n_days = int(last_n_days)
        self.interval = interval
        self.startTime, self.endTime = self.getStartEndTime(self.last_n_days, startTime, endTime)
        self.strategy = strategy
        self.percentage_returns = 0
        self.cash=1
        self.holding=0
        self.ratioChange = 1
        self.latestPrice = self.buyPrice = self.sellPrice = 0
        self.ohlc_data = 0
        
    def refreshData(self, ticker=None, strategy=None, last_n_days=None, interval=None):
        if (ticker!=None):
            self.ticker = ticker
        if (strategy!=None):
            self.strategy = strategy
        if (last_n_days!=None):
            self.last_n_days = int(last_n_days)
        if (interval!=None):
            self.interval = interval
            
        self.startTime, self.endTime = self.getStartEndTime(self.last_n_days, self.startTime, self.endTime)
        self.ohlc_data = self.get_data(self.ticker)


    def getSignalFromStrategy(self, col):
        return self.ohlc_data.tail(1)[col][0]
    
    def getLatestPrice(self):
        self.latestPrice = self.ohlc_data.tail(1)["Adj Close"][0]
        return self.latestPrice
        
    def setCash(self, val):
        self.cash = val