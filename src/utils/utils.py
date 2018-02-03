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
pt_dic=parse_trading_day (strategy_name, pt)
    'name'          strategy name
    'arr'           annualized rate of return
    'barr'          annualized rate of return for benchmark strategy
    'maxd'          maximum drawdown
    'volat'         volatility
    'sharpe'        sharpe ratio
    'alpha'         alpha
    'beta'          beta
'''
#-------------------------------------------------------------------

def strategy_info(strategy_name, pt):
    
    delta_time=pt.index[-1]-pt.index[0]
    pt_dic={}
    np_fund=pt['value'].values+pt['cash'].values

    # strategy name
    pt_dic['name']=strategy_name

    # annualized rate of return
    pt_dic['arr']=((np_fund[-1])/(np_fund[0])-1)/delta_time.days*250.0

    # annualized rate of return for benchmark strategy
    pt_dic['barr']=(pt['base'][-1]/(pt['base'][0])-1)/delta_time.days*250.0

    # maximum drawdown
    pos=1
    maxd=0
    for value in np_fund[1:]:
        if maxd<(1-value/np_fund[0:pos].max()):
            maxd=1-value/np_fund[0:pos].max()
        pos=pos+1
    pt_dic['maxd']=maxd

    return pt_dic 
