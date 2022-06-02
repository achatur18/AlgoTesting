# -*- coding: utf-8 -*-

from .testingCls import BackTestingCls
import pandas as pd


class BackTestingReg(BackTestingCls):
    def numToCatLabel(self, df, col, target_col, uthres=0.3, lthres=-0.3):
        buy_idx=df[col]>uthres
        sell_idx = df[col]<lthres
        
        df[target_col]="HOLD"
        df[target_col][buy_idx]="BUY"
        df[target_col][sell_idx]="SELL"
        
    def makeFlagFromLabels(self,df=None, col='trend', upthres=0.1, lowthres=-0.1):
        if isinstance(df, pd.DataFrame):
            ohlc_data = df.copy()
        elif isinstance(df, pd.Series):
            ohlc_data = pd.DataFrame(df.copy(), columns=[col])
        else:
            ohlc_data = self.ohlc_data
            
            
        buy_=ohlc_data[col]>=upthres
        sell_=ohlc_data[col]<=lowthres
        
        ohlc_data[col]="HOLD"
        ohlc_data[col][buy_]="BUY"
        ohlc_data[col][sell_]="SELL"
        
        if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
            return ohlc_data
        else:
            self.ohlc_data = ohlc_data