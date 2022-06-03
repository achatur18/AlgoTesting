#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 10:13:04 2022

@author: abhaychaturvedi
"""

from AlgoTesting import BackTestingCls


ticker ='BTC-USD'
startTime='2022-05-19'
endTime="2022-05-24"
interval = '5m'
bt=BackTestingCls(ticker=ticker, startTime=startTime, endTime=endTime, interval=interval)

##########################################
####### Making the target label #######
##########################################

inp_columns = ['rsi', "ATR", "ADX", "macd", "signal", "MB", "UB", "LB", "BB_Width"]
target_col = "trend"

bt.movingLabel(label=target_col, window=81, padding=8, shift=0)
#bt.nextLabel(label='trend', window=5)

bt.ohlc_data[target_col]=bt.ohlc_data[target_col].shift(-1)
bt.ohlc_data.drop(["Final Lowerband", "Final Upperband"], axis=1, inplace=True)

##########################################
####### plotting prepaired labels #######
##########################################

color_dict = {"BUY": '#49fc03', "SELL": "#fc0303", "HOLD": '#000000'}

bt.ohlc_data['rank']=range(len(bt.ohlc_data))

s_=0
n_=1400
bt.ohlc_data[s_:n_].plot.scatter(x='rank', y="Adj Close",s=4, color = [color_dict.get(x, '#333333') for x in bt.ohlc_data[target_col]][s_:n_])


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
Y_train = train[target_col]
# Y_train = pd.get_dummies(train, columns = [target_col])[target_columns]

X_test =test[inp_columns]
Y_test = test[target_col]
# Y_test = pd.get_dummies(test, columns = [target_col])[target_columns]

X_train.shape, X_test.shape

########################################
######## Training the model########
########################################

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
 # creating a RF classifier
#clf = DecisionTreeClassifier(max_depth = 3, random_state=0) 
clf = RandomForestClassifier(max_depth = 10, random_state=0, n_estimators=100) 
 
# Training the model on the training dataset
# fit function is used to train the model using the training sets as parameters
# Y_train.isna().sum()
clf.fit(X_train, Y_train)
clf.classes_


pd.DataFrame(clf.feature_importances_, index=X_train.columns)


########################################################
######## perform prediction on complete data ########
########################################################

X_test["pred"] = clf.predict(X_test[inp_columns])

X_test["pred"].value_counts()


########################################################
######## print confusion matrix ########
########################################################
from sklearn.metrics import confusion_matrix
confusion_matrix(Y_test, X_test["pred"])

##########################################
####### Calculate returns on test data #######
##########################################
inp_col = inp_columns.copy()
#inp_col.append("Adj Close")
inp_col.append("pred")
#inp_col.append("trend")


X_test_ =X_test[inp_col].copy()
X_test_['Adj Close'] = test["Adj Close"]

bt.calculateTradeReturns(df_dic= X_test_, flag_column='pred', output_column='return_pred')
print("Returns on strategy: ", bt.percentage_returns)

# Doing return claculation on whole data just to verify the calculateReturns function's 

print("Maximum Return on one-time investment i.e. max draw up: ", bt.calculateInvestmentReturns(df_dic=X_test, type="max_du"))
print("Return on one-time investment", bt.calculateInvestmentReturns(df_dic=X_test, type="complete"))


X_test_['trend'] = Y_test
bt.calculateTradeReturns(df_dic= X_test_, flag_column='trend', output_column='return_trend')
print("Returns on prepaired labels: ", bt.percentage_returns)



print("Accuracy of bids on strategy", bt.calculateAccuracy(df_dic= X_test_,column_name="return_pred"))
print("Accuracy of bids on prepaired labels", bt.calculateAccuracy(df_dic= X_test_, column_name="return_trend"))
