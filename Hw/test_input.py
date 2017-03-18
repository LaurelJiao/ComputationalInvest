import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import sys
import pdb
from scipy.optimize import minimize


def simulate(startyear,startmonth,startday,endyear,endmonth,endday,ls_symbols):
        # Set QSTK object and data from Yahoo
    dt_timeofday = dt.timedelta(hours=16)
    dt_start = dt.datetime(startyear,startmonth,startday)
    dt_end = dt.datetime(endyear,endmonth,endday)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    global Num_of_trading_days
    Num_of_trading_days = len(ldt_timestamps)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    # Daily return
    na_rets = na_normalized_price.copy()
    # Daily portfolio return GLOBAL
    global daily_rets

    daily_rets = na_rets.copy()

def alloc_prob(w):

    return -1*np.sqrt(Num_of_trading_days) * np.mean(np.sum(daily_rets * w, axis=1))/\
    np.std(np.sum(daily_rets * w, axis=1))


# equality constraints for weight allocation 
def econ(w):
    return sum(w)=1


def main():
    if len(sys.argv) != 11:
        print("Wrong number of argument")
    
    # Pass input 
    startyear = int(sys.argv[1])
    startmonth = int(sys.argv[2])
    startday = int(sys.argv[3])
    endyear = int(sys.argv[4])
    endmonth = int(sys.argv[5])
    endday = int(sys.argv[6])
    ls_symbols = [str(sys.argv[7]),str(sys.argv[8]),str(sys.argv[9]),str(sys.argv[10])]
    
    simulate(startyear,startmonth,startday,endyear,endmonth,endday,ls_symbols)

    w0 =[0.1,0.2,0.3,0.4]
    cons = ([{'type': 'eq','fun':econ}],[{'type':'ineq','fun': lambda w: np.array(w[:])}])
    # print(daily_rets)
    # print(Num_of_trading_days)
    # pdb.set_trace()
    res = minimize(alloc_prob,w0, method='nelder-mead',constraints= cons, \
        options={'xtol': 1e-8, 'disp': True})

    print(res.x)


if __name__ == '__main__':
    main()



