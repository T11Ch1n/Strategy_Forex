# _*_ coding: UTF-8 _*_
# Code by chen


import pandas as pd
month = [
    "202201",
    "202202",
    "202202",
    "202203",
    "202204",
    "202204",
    "202205",
    "202206",
    "202207",
    "202208",
    "202209"
]
df_list2022 = [pd.read_csv("Forex_Data/DAT_MT_EURUSD_M1_"+mon+".csv",
                             parse_dates={'DateTime':[0]},
                             usecols=[0,1,2,3,4,5],
                             header=None).set_index("DateTime")
                  for mon in month]
df_list = [pd.read_csv("Forex_Data/DAT_MT_EURUSD_M1_"+str(yr)+".csv",
                             parse_dates={'DateTime':[0]},
                             usecols=[0,1,2,3,4,5],
                             header=None).set_index("DateTime")
                  for yr in range(2012,2022)]
df = pd.concat(df_list + df_list2022)
cols = ['min','open', 'high', 'low', 'close']
df.columns = cols
df.drop(['min'],axis=1,inplace=True)
timeframe = {
    #"h"
    "24h"
}
df_dict = {}
ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close':'last'}
for tf in timeframe:
    df_dict[tf] = df.resample(tf, closed='right', label='right').agg(ohlc_dict)
    df_dict[tf].to_csv("New_Forex_Data/eurusd"+tf+".csv")