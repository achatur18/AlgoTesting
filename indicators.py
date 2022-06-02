# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class Indicators:

    def MACD(self, DF, a=12 ,b=26, c=9):
        """function to calculate MACD
          typical values a(fast moving average) = 12; 
                          b(slow moving average) =26; 
                          c(signal line ma window) =9"""
        df = DF.copy()
        df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
        df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
        df["macd"] = df["ma_fast"] - df["ma_slow"]
        df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
        return df.loc[:,["macd","signal", "ma_slow", "ma_fast"]]

    def ATR(self, DF, n=14):
        "function to calculate True Range and Average True Range"
        df = DF.copy()
        df["H-L"] = df["High"] - df["Low"]
        df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
        df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
        df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
        df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
        return df["ATR"]

    def ADX(self, DF, n=20):
        "function to calculate ADX"
        df = DF.copy()
        df["ATR_"] = self.ATR(DF, n)
        df["upmove"] = df["High"] - df["High"].shift(1)
        df["downmove"] = df["Low"].shift(1) - df["Low"]
        df["+dm"] = np.where((df["upmove"]>df["downmove"]) & (df["upmove"] >0), df["upmove"], 0)
        df["-dm"] = np.where((df["downmove"]>df["upmove"]) & (df["downmove"] >0), df["downmove"], 0)
        df["+di"] = 100 * (df["+dm"]/df["ATR_"]).ewm(alpha=1/n, min_periods=n).mean()
        df["-di"] = 100 * (df["-dm"]/df["ATR_"]).ewm(alpha=1/n, min_periods=n).mean()
        df["ADX"] = 100* abs((df["+di"] - df["-di"])/(df["+di"] + df["-di"])).ewm(alpha=1/n, min_periods=n).mean()
        return df["ADX"]


    def Boll_Band(self, DF, n=14):
        "function to calculate Bollinger Band"
        df = DF.copy()
        df["MB"] = df["Adj Close"].rolling(n).mean()
        df["UB"] = df["MB"] + 2*df["Adj Close"].rolling(n).std(ddof=0)
        df["LB"] = df["MB"] - 2*df["Adj Close"].rolling(n).std(ddof=0)
        df["BB_Width"] = df["UB"] - df["LB"]
        return df[["MB","UB","LB","BB_Width"]]

    def RSI(self, DF, n=14):
        "function to calculate RSI"
        df = DF.copy()
        df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
        df["gain"] = np.where(df["change"]>=0, df["change"], 0)
        df["loss"] = np.where(df["change"]<0, -1*df["change"], 0)
        df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
        df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
        df["rs"] = df["avgGain"]/df["avgLoss"]
        df["rsi"] = 100 - (100/ (1 + df["rs"]))
        return df["rsi"]

    def Supertrend(self, df, atr_period=10, multiplier=3.0):
        
        high = df['High']
        low = df['Low']
        close = df['Adj Close']
        
        # calculate ATR
        price_diffs = [high - low, 
                       high - close.shift(), 
                       close.shift() - low]
        true_range = pd.concat(price_diffs, axis=1)
        true_range = true_range.abs().max(axis=1)
        # default ATR calculation in supertrend indicator
        atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 
        # df['atr'] = df['tr'].rolling(atr_period).mean()
        
        # HL2 is simply the average of high and low prices
        hl2 = (high + low) / 2
        # upperband and lowerband calculation
        # notice that final bands are set to be equal to the respective bands
        final_upperband = upperband = hl2 + (multiplier * atr)
        final_lowerband = lowerband = hl2 - (multiplier * atr)
        
        # initialize Supertrend column to True
        supertrend = [True] * len(df)
        
        for i in range(1, len(df.index)):
            curr, prev = i, i-1
            
            # if current close price crosses above upperband
            if close[curr] > final_upperband[prev]:
                supertrend[curr] = True
            # if current close price crosses below lowerband
            elif close[curr] < final_lowerband[prev]:
                supertrend[curr] = False
            # else, the trend continues
            else:
                supertrend[curr] = supertrend[prev]
                
                # adjustment to the final bands
                if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                    final_lowerband[curr] = final_lowerband[prev]
                if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                    final_upperband[curr] = final_upperband[prev]
    
            # to remove bands according to the trend direction
            if supertrend[curr] == True:
                final_upperband[curr] = np.nan
            else:
                final_lowerband[curr] = np.nan
        
        return pd.DataFrame({
            'Supertrend': supertrend,
            'Final Lowerband': final_lowerband,
            'Final Upperband': final_upperband
        }, index=df.index)
