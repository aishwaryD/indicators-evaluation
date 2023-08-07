from util import get_data
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import indicators as ind


def trades(symbol, sd, ed):
	df = get_data([symbol], pd.date_range(sd, ed))
	price_df = df[[symbol]].ffill().bfill()
	trades_df = df[['SPY']]
	trades_df = trades_df.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
	trades_df[:] = 0
	dates = trades_df.index
	current_pos = 0
	for i in range(len(dates) - 1):
		curr_price = price_df.loc[dates[i]].loc[symbol]
		next_price = price_df.loc[dates[i + 1]].loc[symbol]
		action = 1000 - current_pos if next_price > curr_price else -1000 - current_pos
		trades_df.loc[dates[i]].loc[symbol] = action
		current_pos += action
	return trades_df


def stats(benchmark, theoretical):
	benchmark, theoretical = benchmark['value'], theoretical['value']
	cmr_the = theoretical[-1] / theoretical[0] - 1
	cmr_ben = benchmark[-1] / benchmark[0] - 1
	dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
	dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]
	stddr_ben, stddr_the = dr_ben.std(), dr_the.std()
	avgdr_ben, avgdr_the = dr_ben.mean(), dr_the.mean()
	# print("\n[TheoreticallyOptimalStrategy]")
	# print(f"Cumulative Return: {cmr_the:.6f}")
	# print(f"Stdev of Daily Returns: {stddr_the:.6f}")
	# print(f"Mean of Daily Returns: {avgdr_the:.6f}\n")
	# print("[Benchmark]")
	# print(f"Cumulative Return: {cmr_ben:.6f}")
	# print(f"Stdev of Daily Returns: {stddr_ben:.6f}")
	# print(f"Mean of Daily Returns: {avgdr_ben:.6f}\n")


def benchmark(sd, ed, sv):
	trades_df = get_data(['SPY'], pd.date_range(sd, ed))
	trades_df = trades_df.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
	trades_df[:] = 0
	trades_df.loc[trades_df.index[0]] = 1000
	portvals = compute_portvals(trades_df, sv, commission=0.00, impact=0.00)
	return portvals


def plot_graph(benchmark_portvals, theoretical_portvals):
	benchmark_portvals['value'] /= benchmark_portvals['value'][0]
	theoretical_portvals['value'] /= theoretical_portvals['value'][0]
	fig, ax = plt.subplots(figsize=(14, 8))
	ax.set_title("TheoreticallyOptimalStrategy")
	ax.set_xlabel("Date")
	ax.set_ylabel("Cumulative Return")
	ax.tick_params(axis='x', rotation=30)
	ax.grid()
	ax.plot(benchmark_portvals, label="Benchmark", color="green")
	ax.plot(theoretical_portvals, label="Theoretical", color="red")
	ax.legend()
	plt.savefig("images/theoretical.png", bbox_inches='tight')
	plt.clf()


def testPolicy(symbol, sd, ed, sv):
	df_trades = trades(symbol, sd=sd, ed=ed)
	portvals_the = compute_portvals(df_trades, sv, commission=0.00, impact=0.00)
	portvals_be = benchmark(sd, ed, sv)
	stats(portvals_be, portvals_the)
	plot_graph(portvals_be, portvals_the)
	ind.bollinger_band(sd, ed, symbol, plot=True, window=5)
	ind.price_to_sma(sd, ed, symbol, plot=True, window=14)
	ind.ema(sd, ed, symbol, plot=True, window=20)
	ind.macd(sd, ed, symbol, plot=True)
	ind.tsi(sd, ed, symbol, plot=True)



def author():
	return 'aishwary'


if __name__ == "__main__":
	pass
