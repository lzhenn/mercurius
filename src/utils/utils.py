#!/usr/bin/env python

"Utilities for the trading system"
#-------------------------------------------------------------------------
'''

time_new=parse_trading_day (date.idx, time_obj)
     * shift time obj backward to the nearest trading day



'''
#-------------------------------------------------------------------------
import datetime

def parse_trading_day(date_series, time_obj):
    tdelta=datetime.timedelta(days=1)
    while not (time_obj in date_series):
        time_obj=time_obj-tdelta
    return time_obj


#-------------------------------------------------------------------
'''
pt_dic=parse_trading_day (strategy_name, pd)
    'name'          strategy name
    'arr'           annualized rate of return
    'maxd'          maximum drawdown
    'volat'         volatility
    'sharpe'        sharpe ratio
    'alpha'         alpha
    'beta'          beta
'''
#-------------------------------------------------------------------

def strategy_info(strategy_name, pd):
    pt_dic['name']=strategy_name
    pt_dic['']


    return time_obj
