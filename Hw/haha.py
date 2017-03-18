import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import pdb

Num_Trading_Days = 252

def simulate(dt_start, dt_end, ls_symbols, allocations):

    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    na_price = d_data['close'].values
    # print(na_price)
    na_normalized_price = na_price / na_price[0, :]
    # print(na_normalized_price)
    # Multiply allocations
    na_rets = na_normalized_price.copy()
    # This is the one-day return
    na_portrets = np.sum(na_rets * allocations, axis=1)
    # na_port_total = np.cumprod(na_portrets + 1)
    # na_component_total = np.cumprod(na_rets + 1, axis=0)

    # print("na_porters:")
    # print(na_portrets)
    pdb.set_trace()
    dailyPort = na_portrets.copy()
    tsu.returnize0(dailyPort)

    daily_ret = np.mean(dailyPort)
    vol = np.std(dailyPort)
    sharpe = np.sqrt(Num_Trading_Days) * daily_ret/vol
    cum_ret = na_portrets[na_portrets.shape[0]-1]
    # pdb.set_trace()

    return vol, daily_ret,sharpe,cum_ret

def print_simulate(dt_start,dt_end,ls_symbols,allocations):
    vol,daily_ret,sharpe,cum_ret = simulate(dt_start,dt_end,ls_symbols,allocations)
    print "Start Date: ", dt_start
    print "End Date: ", dt_end
    print "Symbols: ", ls_symbols
    print "Optimal Allocations: ", allocations
    print "Sharpe Ratio: ", sharpe
    print "Volatility: ", vol
    print "Average Daily Return: ",daily_ret
    print "Cumulative Return: ", cum_ret

def Optimizer(dt_start, dt_end,ls_symbols):

    max_alloc = [0.0,0.0,0.0,0.0]
    max_sharpe = -1

    for i in range(0,11):
                for j in range(0,11-i):
                        for k in range(0,11-i-j):
                                for l in range (0,11-i-j-k):
                                        if (i + j + l + k) == 10:
                                                alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                                                vol, daily_ret, sharpe, cum_ret = simulate( dt_start, dt_end, ls_symbols, alloc )
                                                if sharpe > max_sharpe:
                                                        max_sharpe = sharpe
                                                        max_alloc = alloc
    return max_alloc

    

def main():
    ls_symbols = ["AAPL", "GLD", "GOOG","XOM"]
    dt_start = dt.datetime(2011,1,1)
    dt_end = dt.datetime(2011,12,31)
    allocations = [0.1,0.1,0.1,0.7]

    max_alloc = Optimizer(dt_start,dt_end,ls_symbols)
    print_simulate(dt_start,dt_end,ls_symbols,max_alloc)
    # pdb.set_trace()


if __name__ == "__main__":
    main()