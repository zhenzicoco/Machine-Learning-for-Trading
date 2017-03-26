"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd,ed,syms,allocs,sv,rfr,sf,gen_plot):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms] # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    # Get daily portfolio value
    port_val = (prices/prices.ix[0,:]*allocs*sv).sum(axis=1) # add code here to compute daily portfolio values
    # Get portfolio statistics (note: std_daily_ret = volatility)
    
    daily_rets=(port_val/port_val.shift(1)-1).ix[1:]
    #calculate cumulative return
    cr=port_val[-1]/port_val[0]-1
    #calculate average daily return
    adr=daily_rets.mean()
    #calculate standard deviation of daily return
    sddr=daily_rets.std()
    #calculate Sharp Ratio
    sr=np.sqrt(sf)*((daily_rets-rfr).mean())/daily_rets.std()
    
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp=(df_temp/df_temp.ix[0,:])
        plot_data(df_temp)
        pass

    # Add code here to properly compute end value
    #calculate end value
    ev = port_val[-1]
    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,06,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        rfr=risk_free_rate,\
        sf=sample_freq,\
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
    print "End value of portfolio:",ev
    
if __name__ == "__main__":
    test_code()
