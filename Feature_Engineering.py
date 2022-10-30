# _*_ coding: UTF-8 _*_
# Code by chen

import pandas as pd
import numpy as np

def MACD(df, period1, period2, periodSignal):
    EMA1 = pd.DataFrame.ewm(df,span=period1).mean() # Provides exponential weighted functions
    EMA2 = pd.DataFrame.ewm(df,span=period2).mean()

    MACD = EMA1-EMA2
    Signal = pd.DataFrame.ewm(MACD,periodSignal).mean()

    Histogram = MACD-Signal
    return Histogram

def stochastics_oscillator(df,period):
    l = pd.DataFrame.rolling(df, period).min()
    h = pd.DataFrame.rolling(df, period).max()
    k = 100 * (df - l) / (h - l)
    return k

def ATR(high, low, close):
    # Method A: Current High less the current Low
    f = pd.DataFrame()
    f['high'] = high
    f['low'] = low
    f['close'] = close
    f['H-L'] = abs(f.high - f.low)
    f['H-PC'] = abs(f.high - f.close.shift(1))
    f['L-PC'] = abs(f.low - f.close.shift(1))
    TR = f[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    return TR.values

def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = (u.ewm(com=period-1, adjust=False).mean()) / (d.ewm(com=period-1, adjust=False).mean().abs())
    return 100 - 100 / (1 + rs)

def SMA(price,N):
    SMA = price.rolling(N).mean()
    return SMA


def EWMA(price, N):
    EWMA = price.ewm(span=N).mean()
    return EWMA


def CCI(priceHIGH, priceLOW, priceCLOSE, N):
    TP = (priceHIGH + priceLOW + priceCLOSE) / 3
    CCI = (TP - TP.rolling(N).mean()) / (0.015 * TP.rolling(N).std())
    return CCI

def STOK(close, low, high,N):
    STOK = ((close - low.rolling(N).min()) / (high.rolling(N).max() - low.rolling(N).min())) * 100
    return STOK

def STOD(close, high, low, N):
    STOK = ((close - low.rolling(N).min()) / (high.rolling(N).max() - low.rolling(N).min())) * 100
    STOD = STOK.rolling(3).mean()
    return STOD

def MTM(price, periods=1):
    return (pd.DataFrame(price) - pd.DataFrame(price).shift(periods)).iloc[:, 0]

def acc_pri_change_abs(price,periods=10):
    return abs((price - price.shift(1))/price.shift(1)).rolling(periods).sum()

def acc_pri_change(price,periods=10):
    return (price - price.shift(1))/price.shift(1).rolling(periods).sum()

