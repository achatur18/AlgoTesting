# -*- coding: utf-8 -*-

import datetime as dt

class Utility:

    def drop_na(self, ohlc_mon=None):
        if ohlc_mon==None:
          ohlc_mon=self.ohlc_data.copy()

        ohlc_mon.dropna(inplace=True,how="any")    
        self.ohlc_data = ohlc_mon

    def getStartEndTime(self, last_n_days, startTime, endTime):
        if (startTime and endTime):
# =============================================================================
#           dateType = type(dt.datetime.today())
#           assert type(startTime)==dateType, "Please provide datetime in correct format"
#           assert type(endTime)==dateType, "Please provide datetime in correct format"
# =============================================================================
          return startTime, endTime
        assert type(last_n_days)==type(0), "Please provide last_n_days in integer format"
        start = dt.datetime.today()-dt.timedelta(last_n_days)
        end = dt.datetime.today()
        return start, end


    def slope(self, column_name, window=11, shift_=0):
        ohlc_data = self.ohlc_data
        ohlc_data['slope_'+column_name] = ohlc_data[ticker][column_name].rolling(window).apply(lambda x: (x[-1]-x[0])/window) 
        ohlc_data['slope_'+column_name] = ohlc_data[ticker]['slope_'+column_name].shift(shift_)
            