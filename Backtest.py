# _*_ coding: UTF-8 _*_
# Code by chen

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def simulation(signal_file, market_file):
    capital = 100000
    cost_rate = 0
    annual_trading_days = 244

    market_data = pd.read_csv(market_file, parse_dates=["Date"], index_col="Date")
    signal = pd.read_csv(signal_file, parse_dates=["Date"], index_col="Date")

    a = market_data.index
    b = signa.index
    start_time = max(min(a), min(b))
    end_time = min(max(a), max(b)
    market_data = market_data[start_time:end_time]
    signal = signal[start_time:end_time]

    market_data["return"] = market_data['close'] - market_data['open']
    market_data["abs_return"] = abs(market_data["return"])
    market_data["label"] = market_data["return"].apply(lambda: 1 if x > 0 else 0)
    market_data["signal"] = signal["signal"]
    market_data["daily_P"] = market_data["abs_return"][market_data["label"] == market_data["signal"]]
    market_data["daily_L] = -market_data["abs_return"][market_data["label"]]!=market_data["signal"]
    market_data["daily_P"].fillna(0, inplace=True)
    market_data["daily_L"].fillna(0, inplace=True)
    market_data["daily_gross_PNL"] = (market_data["daily_P"] + market_data["daily_L"]) * signal["quantity"]

    market_data["equity"] = market_data["daily_PNL"].cumsum() + capital
    equity = market_data["equity"].tolist()
    max_drawdown = [1 - x / (max(equity[0:equity.index(x) + 1])) for x in equity]
    max_drawdown = [x * 100 for x in max_drowndown]
    market_data["max_drawdown"] = max_drawdown
    MDD = max(max_drawdown) / 100

    PNL = market_data["daily_PNL"].sum()
    trade_period = len(market_data)
    annualized_return = PNL / capital / trade_period * annual_trading_days

    market_data["tran_cost"] = (market_data["close"] + market_data["open"]) * signal["quantity"] * cost_rate
    tran_cost = market_data["tran_cost"].sum()

    market_data["daily_PNL"] = market_data["daily_gross_PNL"] - market_data["tran_cost"]
    market["win?"] = market_data["daily_PNL"].apply(lambda x: 1 if x > 0 else 0)

    win_days = len(market_data[market_data["daily_PNL"] > 0])
    loss_days = len(market_data[market_data["daily_PNL"] <= 0])
    win_rate = win_days / trade_period
    loss_rate = loss_days / trade_period

    base_quantity = np.floor(capital / market_data.loc[market_data.index[0], "open"])
    base_daily_PNL = market_data["return"] * base_quantity
    market_data["base_equity"] = base_daily_PNL.cumsum() + capital

    avg_daily_PNL = market_data["daily_PNL"].mean()
    vol_daily_PNL = market_data["daily_PNL"].std()
    base_avg_daily_PNL = (base_daily_PNL / market_data["base_equity"].shift(1)).mean()
    base_vol_daily_PNL = (base_daily_PNL / market_data["base_equity"].shift(1)).std()

    strategy_sr = avg_daily_PNL / vol_daily_PNL * np.sqrt(annual_trading_days)
    base_sr = base_avg_daily_PNL / base_vol_daily_PNL * np.sqrt(annual_trading_days)

    ## output a json file which contains all the stats.
    output = {"capital": capital, "PNL": PNL, "trade_period": trade_period,
              "annualized_return": annualized_return, "win_days": win_days, "loss_days": loss_days,
              "win_rate": win_rate,
              "tran_cost": tran_cost,
              "avg_daily_PNL": avg_daily_PNL, "vol_daily_PNL": vol_daily_PNL, "strategy_sr": strategy_sr,
              "base_sr": base_sr,
              "max_drawdown": MDD}

    with open("output.json", "w") as g:
        json.dump(output, g)

    ## output a report table which contains some core stats
    report_table = market_data[["signal", "label", "win?", "daily_PNL", "equity"]]
    report_table.to_csv("report_table.csv")

    return report_table, output, market_dat


def plot_figure(market_data):
    ## input the market_data generated from the simulation
    ## output a plot containning equity & max drawdown & base equity curve.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(market_data['equity'], label="equity")
    ax.plot(market_data["base_equity"], 'y', label="base")
    ax2 = ax.twinx()
    ax2.plot(market_data["max_drawdown"], 'r', label="max drawdown")

    ax.set_xlabel('Time')
    ax.set_ylabel('Equity')
    ax2.set_ylabel('Max Drawdown')
    fmt = '%.3f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax2.yaxis.set_major_formatter(yticks)
    ax2.set_ylim((0, 50))
    ax.legend(loc='center left')
    ax2.legend(loc='center right')
    plt.savefig("output.png")
    plt.show()

    return fig

