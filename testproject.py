import TheoreticallyOptimalStrategy as tos
import datetime as dt


def author():
    return 'aishwary'


if __name__ == "__main__":
    df_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
