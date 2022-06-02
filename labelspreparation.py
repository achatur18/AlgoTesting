# -*- coding: utf-8 -*-
import numpy as np

def sinx_(x):
    return x/((1+x**2)**0.5)

class LabelsPreparation:
    
    def nextLabel(self, window=1, label='trend'):
        ohlc_data = self.ohlc_data
        ohlc_data[label+"_"+str(window)] = ohlc_data["Adj Close"].rolling(window).mean().shift(-window)
        ohlc_data[label] = np.where(ohlc_data[label+"_"+str(window)]>ohlc_data["Adj Close"], "BUY", "SELL")
        ohlc_data[label] = np.where(ohlc_data[label+"_"+str(window)]<ohlc_data["Adj Close"], "SELL", ohlc_data[label])
        
    def movingSlopeLabel(self, window=5, label="trend", shift_=-5):
        ohlc_data = self.ohlc_data
        ohlc_data[label] = ohlc_data["Adj Close"].rolling(window).apply(lambda s: sinx_(np.polyfit(s, np.arange(len(s)), 1)[0]))
        ohlc_data[label] = ohlc_data[label].shift(shift_)
        
    def weightedMovSlopeLabel(self, label='trend', window_s=30, window_l=80, shift_s=-30, shift_l=-80, weight_s=0.5):
        self.movingSlopeLabel(label='trend_s', window=window_s, shift_=shift_s)
        self.movingSlopeLabel(label='trend_l', window=window_l, shift_=shift_l)
        self.ohlc_data[label]=(self.ohlc_data['trend_s']*weight_s)+(self.ohlc_data['trend_l']*(1-weight_s))
        
        
    def movingLabel(self, window=11, label="trend", padding=0, shift=-1):
        ohlc_data = self.ohlc_data
        ohlc_data["max_"+label] = ohlc_data["Adj Close"].rolling(window).max()
        ohlc_data["min_"+label] = ohlc_data["Adj Close"].rolling(window).min()
        ohlc_data["max_"+label] = ohlc_data["max_"+label].shift(-1*(window//2))
        ohlc_data["min_"+label] = ohlc_data["min_"+label].shift(-1*(window//2))
        
        ohlc_data[label]='HOLD'
                    
        sell_idx=[]
        for val in np.where(ohlc_data["Adj Close"]==ohlc_data["max_"+label]):
            for i in range(-padding, padding+1):
                sell_idx.append(i+val)
        sell_idx = np.concatenate(sell_idx, axis=0)+shift
        ohlc_data[label][sell_idx] = "SELL"
    
        buy_idx=[]
        for val in np.where(ohlc_data["Adj Close"]==ohlc_data["min_"+label]):
            for i in range(-padding, padding+1):
                buy_idx.append(i+val)
        buy_idx = np.concatenate(buy_idx, axis=0)+shift
        ohlc_data[label][buy_idx] = "BUY"
            