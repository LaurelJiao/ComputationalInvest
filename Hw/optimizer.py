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
import cvxpy as cvx
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
    tsu.returnize0(daily_rets)

def alloc_prob(x):

    return -1*np.sqrt(Num_of_trading_days) * np.mean(np.dot(daily_rets,x))/np.std(np.dot(daily_rets,x)) + sum(-0.001*np.log(x))


# equality constraints for weight allocation 
# def econ(w):
#     return sum(w[:])=1


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
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    simulate(startyear,startmonth,startday,endyear,endmonth,endday,ls_symbols)

    x0 =[0.1,0.2,0.3,0.4]
    print(alloc_prob(x0))
    # pdb.set_trace()
    # cvx convex solver
    # w = cvx.Variable(4)
    # constraints = [sum(w)==1, w>=0]
    # obj = cvx.Minimize(alloc_prob(w))
    # prob = cvx.Problem(obj, constraints)
    # prob.solve()
    # print "status:", prob.status
    # print "optimal value:", prob.value
    # print "optimal weight:", w.value
    # scipy minimize
    cons = ({'type': 'eq', 'fun': lambda x: 1-sum(x)})

    bnds = ((0,0.1),(0,0.1),(0,0.1),(0,0.1))
    # cons = ({'type': 'ineq', 'fun': c1},
    #         {'type': 'ineq', 'fun': c2},
    #         {'type': 'ineq', 'fun': c3})
    # pdb.set_trace()
    res = minimize(alloc_prob, x0,constraints=cons, method='SLSQP',
        options={'disp': True})

    print(res.x)
    print()


if __name__ == '__main__':
    main()



