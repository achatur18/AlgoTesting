# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt

from AlgoTesting import BackTestingReg

class Saving:
    def saveStrategiesCsv(self, strategies=[], candle='1m', freq=1, totaldays=28, ticker='BTC-USD', filename='result.csv'):
        d={}
            
        for strategy in strategies:
            returns = []
            for i in range(0, totaldays, freq): 
                print(i)
                start=dt.datetime.now()-dt.timedelta((i+freq))
                end=dt.datetime.now()-dt.timedelta(i)
                
                bt=BackTestingReg(ticker, startTime=start, endTime=end, interval=candle)
                
                ########################################################
                ######## Getting different indicators########################
                ################################################################
                bt.get_indicators()
                bt.ohlc_data.drop(['Final Lowerband', 'Final Upperband'], axis=1, inplace = True)
                bt.ohlc_data['macd_prev']=bt.ohlc_data['macd'].shift(1)
                bt.ohlc_data['signal_prev']=bt.ohlc_data['signal'].shift(1)
                
                bt.ohlc_data['rsi_2'] = bt.RSI(bt.ohlc_data, n=2)
                bt.ohlc_data['Supertrend_slow'] = bt.Supertrend(bt.ohlc_data, atr_period=20, multiplier=5)['Supertrend']

                bt.drop_na()
                
                ########################################################
                ######## Implement strategy ########################
                ################################################################
                bt.implementStrategy(strategy=strategy)
                bt.drop_na()
                
                    
                ########################################################
                ######## Shifting labels ########################
                ################################################################
                flag_column='flag'
                bt.ohlc_data[flag_column] = bt.ohlc_data[flag_column].shift(1)
                bt.ohlc_data.fillna(0, inplace=True)
                
                
                ########################################################
                ######## Calculate returns ########################
                ################################################################
                bt.calculateTradeReturns(flag_column=flag_column, output_column='return_flag')
                returns.append(bt.percentage_returns)
# =============================================================================
#                 print("Returns on strategy: ", bt.percentage_returns)
# =============================================================================
            d[strategy.__name__] = returns[::-1]
        
        d=pd.DataFrame(d)
        d.to_csv(filename)
        
        d.cumprod().to_csv(filename.split('.')[0]+"_cum.csv")

        return d
