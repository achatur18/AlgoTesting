# -*- coding: utf-8 -*-
import numpy as np
from tqdm import tqdm
import pandas as pd

class Sampling:
    def CumsumSampling(self, df, col, threshold):
        """
        :param raw_price: (series) of close prices.
        :param threshold: (float) when the abs(change) is larger than the threshold, the
        function captures it as an event.
        :return: (datetime index vector) vector of datetimes when the events occurred. This is used later to sample.
        """
        print('Applying Symmetric CUSUM filter.')
        raw_price = df[col]
    
        t_events = []
        s_pos = 0
        s_neg = 0
    
        # log returns
        #diff = np.log(raw_price).diff().dropna()
        diff = (raw_price).diff().dropna()
    
        # Get event time stamps for the entire series
        for i in tqdm(diff.index[1:]):
            pos = float(s_pos + diff.loc[i])
            neg = float(s_neg + diff.loc[i])
            s_pos = max(0.0, pos)
            s_neg = min(0.0, neg)
    
            if s_neg < -threshold:
                s_neg = 0
                t_events.append(i)
    
            elif s_pos > threshold:
                s_pos = 0
                t_events.append(i)
    
        event_timestamps = pd.DatetimeIndex(t_events)
        return t_events