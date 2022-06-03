#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:37:37 2022

@author: abhaychaturvedi
"""

import warnings
warnings.simplefilter(action='ignore')


from AlgoTesting import BackTestingReg
import numpy as np

#tickers='WIPRO.NS'
tickers='RELIANCE.NS'
#tickers='BTC-USD'
bt=BackTestingReg(tickers, last_n_days=3650*2, interval='1d')

bt.ohlc_data.shape

#################################################
####### Defining input and output columns #######
#################################################

inp_columns = ['rsi', "ATR", "ADX", "macd", "signal", "MB", "UB", "LB", "BB_Width"]
target_col_num='trend_num'
target_col_cat = 'trend_cat'

##########################################
####### Making the target label #######
##########################################

# make returns on this
bt.movingLabel(label="trend_mov", window = 80, padding =5)
color_dict = {"BUY": '#49fc03', "SELL": "#fc0303", "HOLD": '#000000'}
bt.coloured_plot(df=bt.ohlc_data, col="trend_mov", color_dict=color_dict)

# 30, 80 for wipro and weight_s = 0.6 
s_=30
l_=80
shift_=0.6


bt.weightedMovSlopeLabel(label=target_col_num, window_s=s_, window_l=l_, shift_s=-int(s_*shift_), shift_l=-int(l_*shift_), weight_s=0.9)

########################################################
######## Plot prepared labels based on color ########
########################################################
uthres=0.1
lthres=-0.1
bt.numToCatLabel(bt.ohlc_data, target_col_num, target_col_cat, uthres=uthres, lthres=lthres)

bt.coloured_plot(bt.ohlc_data, target_col_cat, color_dict)


print(bt.ohlc_data[target_col_num].min(), bt.ohlc_data[target_col_num].max())


########################################################
######## Prepare Indicators ########
########################################################

bt.get_indicators()
bt.ohlc_data.drop(["Final Lowerband", "Final Upperband"], axis=1, inplace=True)

####################################################
####### Train test and input output  split ########
########################################################
import pandas as pd

bt.drop_na()
len_data=bt.ohlc_data.shape[0]

train_split_=0.5

train = bt.ohlc_data[:int(len_data*train_split_)]
test = bt.ohlc_data[int(len_data*train_split_):]

X_train = train[inp_columns]
Y_train = train[target_col_num]
# Y_train = pd.get_dummies(train, columns = [target_col])[target_columns]

X_test =test[inp_columns]
Y_test = test[target_col_num]
# Y_test = pd.get_dummies(test, columns = [target_col])[target_columns]

X_train.shape, X_test.shape


########################################
######## Training the model########
########################################

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor

clf = RandomForestRegressor(max_depth = 5, random_state=0, n_estimators=100) 
 
clf.fit(X_train, Y_train)

pd.DataFrame(clf.feature_importances_, index=X_train.columns)


########################################################
######## Plot graph based on color on trainingdata ########
########################################################
X_train_=X_train.copy()
X_train_["Adj Close"]=train["Adj Close"]
X_train_["pred_num"] = clf.predict(X_train_[inp_columns])

uthres=0.1
lthres=-0.08
bt.numToCatLabel(X_train_, "pred_num", "pred_cat", uthres=uthres, lthres=lthres)

bt.coloured_plot(X_train_, "pred_cat", color_dict)

########################################################
######## perform prediction on complete data ########
########################################################

X_test["pred_num"] = clf.predict(X_test[inp_columns])

X_test["pred_num"].value_counts().sort_index().plot()

########################################################
######## Plot graph based on color on trainingdata ########
########################################################
X_test_=X_test.copy()
X_test_["Adj Close"]=test["Adj Close"]
X_test_["pred_num"] = clf.predict(X_test_[inp_columns])

X_test_['trend_num']=test['trend_num']
X_test_['trend_cat']=test['trend_cat']

bt.numToCatLabel(X_test_, "pred_num", "pred_cat", uthres=uthres, lthres=lthres)

bt.coloured_plot(X_test_, "pred_cat", color_dict)

# =============================================================================
# ########################################################
# ######## print confusion matrix ########
# ########################################################
# from sklearn.metrics import confusion_matrix
# confusion_matrix(bt.makeFlagFromLabels(Y_test, col='trend'), X_test["pred"])
# =============================================================================

##########################################
####### Calculate returns on test data #######
##########################################

bt.calculateTradeReturns(df_dic= X_test_, flag_column='pred_cat', output_column='return_pred')
print("Returns on strategy: ", bt.percentage_returns)

# Doing return claculation on whole data just to verify the calculateReturns function's 

print("Maximum Return on one-time investment i.e. max draw up: ", bt.calculateInvestmentReturns(df_dic=X_test, type="max_du"))
print("Return on one-time investment", bt.calculateInvestmentReturns(df_dic=X_test, type="complete"))

bt.calculateTradeReturns(df_dic= X_test_, flag_column='trend_cat', output_column='return_trend')
print("Returns on prepaired labels 'trend_cat': ", bt.percentage_returns)

bt.calculateTradeReturns(df_dic= test[["trend_mov", "Adj Close"]], flag_column='trend_mov', output_column='return_trend')
print("Returns on prepaired labels 'trend_mov': ", bt.percentage_returns)

print("Accuracy of bids on prepaired labels", bt.calculateAccuracy(df_dic= X_test_, column_name="return_trend"))
#print("Accuracy of bids on strategy", bt.calculateAccuracy(df_dic= X_test_,column_name="return_pred"))

##########################################
####### plotting prepaired labels #######
##########################################
X_test_.min()


X_test_['trend_cat'].value_counts()

bt.coloured_plot(df=X_test_, col=target_col_cat, color_dict=color_dict)

