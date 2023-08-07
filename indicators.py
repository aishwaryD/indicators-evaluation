import pandas as pd
from util import get_data
import datetime as dt
import matplotlib.pyplot as plt


def author():
    return 'aishwary'


def bollinger_band(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), symbol=['JPM'], plot=False, window=5):
    """First indicator: Bollinger Bands"""

    price = get_data([symbol], pd.date_range(sd, ed))
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    if symbol != 'SPY':
        price.drop(['SPY'], axis=1, inplace=True)
    sma = price.copy().rolling(window).mean()
    stdev = price.copy().rolling(window).std()
    upper = sma + 2 * stdev
    upper.rename(columns={sma.columns[0]: 'Upper Band'}, inplace=True)
    lower = sma - 2 * stdev
    lower.rename(columns={sma.columns[0]: 'Lower Band'}, inplace=True)
    sma.rename(columns={sma.columns[0]: 'mean'}, inplace=True)

    if plot:
        plt.figure(figsize=(8, 4))
        plt.gcf().clear()
        plt.plot(price.index, price, label='Price')
        plt.plot(price.index, sma, label='SMA')
        plt.plot(price.index, upper, label='Upper Band')
        plt.plot(price.index, upper, label='Lower Band')
        plt.ylabel('Value')
        plt.xlabel('Date')
        plt.title('Indicator: Bollinger Band')
        plt.legend(loc='best')
        plt.savefig('images/bollinger_indicator.png', bbox_inches='tight')
        plt.gcf().clear()

    return price, sma, upper, lower


def price_to_sma(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), symbol='JPM', plot=False, window=14):
    """Second indicator: price/SMA"""

    price = get_data([symbol], pd.date_range(sd, ed))
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    if symbol != 'SPY':
        price.drop(['SPY'], axis=1, inplace=True)
    price = price/price.iloc[0, 0]
    sma = price.copy().rolling(window).mean()
    price_by_sma = price / sma

    if plot:
        plt.figure(figsize=(8, 4))
        plt.gcf().clear()
        plt.plot(price.index, price, label='Price')
        plt.plot(price.index, sma, label='SMA')
        plt.plot(price.index, price_by_sma, label='Price/SMA')
        plt.ylabel('Value')
        plt.xlabel('Date')
        plt.title('Indicator: Price / SMA')
        plt.legend(loc='best')
        plt.savefig('images/price_sma_indicator.png', bbox_inches='tight')
        plt.gcf().clear()

    return price, sma, price_by_sma


def ema(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), symbol='JPM', plot=False, window=20):
    """Third indicator: Exponential Moving Average"""
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window * 2), ed))
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    if symbol != 'SPY':
        prices.drop(['SPY'], axis=1, inplace=True)
    ema_df = prices[symbol].ewm(span=window, adjust=False).mean()[sd:]
    ema_df /= ema_df[0]
    prices_df = prices[symbol][sd:]
    prices_df /= prices_df[0]
    if plot:
        plt.figure(figsize=(14, 8))
        plt.xticks(rotation=30)
        plt.grid()
        plt.title("EMA of {} days".format(window))
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.plot(prices_df, label="Normalized Price", color="purple")
        plt.plot(ema_df, label="EMA of {} days".format(window), color="red")
        plt.legend()
        plt.savefig("images/ema_indicator.png", bbox_inches='tight')
        plt.clf()
    return ema_df


def macd(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), symbol='JPM', plot=False):
    """Fourth indicator: MACD"""
    df_price = get_data([symbol], pd.date_range(sd - dt.timedelta(52), ed))
    df_price = df_price[[symbol]].ffill().bfill()
    ema1 = df_price.ewm(span=12, adjust=False).mean()
    ema2 = df_price.ewm(span=26, adjust=False).mean()
    macd_raw = ema1 - ema2
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()
    df_price = df_price[sd:]
    ema1 = ema1[sd:]
    ema2 = ema2[sd:]
    macd_raw = macd_raw[sd:]
    macd_signal = macd_signal[sd:]

    if plot:
        fig = plt.figure(figsize=(14, 8))
        plt.suptitle("MACD")
        plt.xlabel("Date")
        plt.ylabel('Normalized Price')
        normalized_ema1 = ema1[symbol] / ema1[symbol][0]
        normalized_ema2 = ema2[symbol] / ema2[symbol][0]
        normalized_df_price = df_price[symbol] / df_price[symbol][0]
        ax1 = plt.subplot(211)
        ax1.plot(normalized_ema1, label="EMA of 12 days", color="orange")
        ax1.plot(normalized_ema2, label="EMA of 26 days", color="red")
        ax1.plot(normalized_df_price, label="Normalized Price", color="purple")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized Price')
        ax1.grid()
        ax2 = plt.subplot(212)
        ax2.plot(macd_raw, label="MACD", color="orange")
        ax2.plot(macd_signal, label="MACD Signal", color="red")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()
        fig.autofmt_xdate()
        plt.savefig("images/macd_indicator.png", bbox_inches='tight')
        plt.clf()

    return macd_raw, macd_signal


def tsi(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), symbol='JPM', plot=False):
    """Fifth indicator: TSI"""
    price = get_data([symbol], pd.date_range(sd-dt.timedelta(50), ed))[symbol].ffill().bfill()
    diff = price.diff()
    ema1 = diff.ewm(span=25, adjust=False).mean()
    ema2 = ema1.ewm(span=13, adjust=False).mean()
    abs_diff = abs(diff)
    abs_ema1 = abs_diff.ewm(span=25, adjust=False).mean()
    abs_ema2 = abs_ema1.ewm(span=13, adjust=False).mean()
    tsi_df = ema2 / abs_ema2
    tsi_df = tsi_df[sd:]
    if plot:
        fig = plt.figure(figsize=(14, 8))
        plt.suptitle("TSI")
        plt.xlabel("Date")
        plt.ylabel('Ratio')
        normalized_df_price = price / price[0]
        ax1 = plt.subplot(211)
        ax1.plot(normalized_df_price, label="Normalized Price", color="purple")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized price')
        ax1.grid()
        ax2 = plt.subplot(212)
        ax2.plot(tsi_df, label="TSI", color="orange")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()
        fig.autofmt_xdate()
        plt.savefig("images/tsi_indicator.png", bbox_inches='tight')
        plt.clf()
    return tsi_df


if __name__ == "__main__":
    pass



