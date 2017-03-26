"""MC1-P2: Optimize a portfolio."""
#CS7646 ywang3234 Yue Wang
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
            
    allocs_initial=np.ones(len(syms))/len(syms)
    allocs_bounds=tuple([(0,1)]*len(syms))
    
    # add code here to find the allocations
    allocs_result=spo.minimize(sharp_ratio_func,allocs_initial,args=(prices,),
                               bounds=allocs_bounds,
                               constraints={'type':'eq','fun':lambda inputs:1.0 - np.sum(inputs)},
                               method='SLSQP',options={'disp':True})
                              
    allocs=allocs_result.x
    # add code here to compute stats
    # Get daily portfolio value
    port_val = (prices/prices.ix[0,:]*allocs).sum(axis=1)
    daily_rets=(port_val/port_val.shift(1)-1).ix[1:]
    #calculate cumulative return
    cr=port_val[-1]/port_val[0]-1
    #calculate average daily return
    adr=daily_rets.mean()
    #calculate standard deviation of daily return
    sddr=daily_rets.std()
    #calculate Sharp Ratio
    sr=np.sqrt(252)*((daily_rets-0).mean())/daily_rets.std()

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp=(df_temp/df_temp.ix[0,:])
        compare_plot=df_temp.plot()
        compare_plot.set_title('Daily Portfolio Value and SPY \n Symbols:{}'.format(syms),y=1.05,fontsize=13)
        compare_plot.set_xlabel('Date',fontsize=12)
        compare_plot.set_ylabel('Price',fontsize=12)
        compare_fig=plt.gcf()
        compare_fig.savefig('plot.png',bbox_inches='tight')
        plt.show()
        pass

    return allocs, cr, adr, sddr, sr    

def sharp_ratio_func(allocs,prices):
    # Get daily portfolio value
    port_val = (prices/prices.ix[0,:]*allocs).sum(axis=1) # add code here to compute daily portfolio values
    # Get portfolio statistics (note: std_daily_ret = volatility)
    daily_rets=(port_val/port_val.shift(1)-1).ix[1:]
    #calculate Sharp Ratio
    sr=np.sqrt(252)*((daily_rets).mean())/daily_rets.std()
    return -sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,06,01)
    end_date = dt.datetime(2011,06,01)
    symbols = ['IBM','X','GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
