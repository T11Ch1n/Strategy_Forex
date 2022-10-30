# _*_ coding: UTF-8 _*_
# Code by chen

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import datetime
from sklearn.metrics import accuracy_score,confusion_matrix
from Feature_Engineering import MACD,ATR,RSI,SMA,EWMA,CCI,STOK,STOD,MTM,acc_pri_change_abs
import itertools
from sklearn.model_selection import cross_validate
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

df_raw = pd.read_csv("New_Forex_data/eurusd24h.csv")
df_raw.set_index('DateTime',inplace=True)
df = df_raw.dropna()
forex = df
Predictors_raw = pd.DataFrame({"sma10":SMA(forex.close.shift(1),10),
                               "sma20":SMA(forex.close.shift(1),20),
                               "MACD":MACD(forex.close.shift(1),12,26,9),
                               "EWMA10":EWMA(forex.close.shift(1), 10),
                               "EWMA20":EWMA(forex.close.shift(1), 20),
                               "RSI":RSI(forex.close.shift(1),20),
                               "ATR":ATR(forex.high.shift(1),forex.low.shift(1),forex.close.shift(1)),
                               "MTM":MTM(forex.close.shift(1), periods=1)
                              })
Predictors = Predictors_raw.dropna()
Target_raw = pd.DataFrame({"value":forex.close.diff()})
Target = Target_raw.dropna()
x_train = Predictors["2012":"2021"]
x_test = Predictors["2021":"2023"]
y_train = Target["2012":"2021"]
y_test = Target["2021":"2023"]

def Get_binary(val):
    if val > 0:
        return 1
    else:
        return 0

a = x_train.index
b = y_train.index
start_time = max(min(a),min(b))
end_time = min(max(a),max(b))
y_train = y_train[start_time:end_time]

Classifier = xgb.sklearn.XGBClassifier(gamma=0.0,
                                       n_estimators=150,
                                       base_score=0.5,
                                       colsample_bytree=1,
                                       learning_rate=0.1)
model = Classifier.fit(x_train,y_train.value.apply(Get_binary))
y_predicted = model.predict(x_test)