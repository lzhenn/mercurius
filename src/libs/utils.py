#!/usr/bin/env python

"Utilities for the trading system"

import datetime
import numpy as np
import hashlib

#-------------------------------------------------------------------------
'''

time_new=parse_trading_day (date.idx, time_obj)
     * shift time obj backward to the nearest trading day



'''
#-------------------------------------------------------------------------
def parse_trading_day(date_series, time_obj):
    tdelta=datetime.timedelta(days=1)
    while not (time_obj.date() in date_series):
        time_obj=time_obj-tdelta
    return time_obj

#-------------------------------------------------------------------------
'''

time_new=parse_trading_day_foreward (date.idx, time_obj)
     * shift time obj foreward to the nearest trading day



'''
#-------------------------------------------------------------------------
def parse_trading_day_foreward(date_series, time_obj):
    tdelta=datetime.timedelta(days=1)
    while not (time_obj in date_series):
        time_obj=time_obj+tdelta
    return time_obj



#-------------------------------------------------------------------
'''
pt_dic=strategy_info(strategy_name, pt)
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
    
    trading_days_per_year=250.0
    norisk_ratio=0.03
    delta_time=pt.index[-1]-pt.index[0]
    pt_dic={}
    np_fund=pt['value'].values+pt['cash'].values

    # strategy name
    pt_dic['name']=strategy_name

    # annualized rate of return
    pt_dic['arr']=((np_fund[-1])/(np_fund[0])-1)/delta_time.days*trading_days_per_year

    # annualized rate of return for benchmark strategy
    pt_dic['barr']=(pt['base'][-1]/(pt['base'][0])-1)/delta_time.days*trading_days_per_year

    # maximum drawdown and volatility
    pos=1
    maxd=0
    for value in np_fund[1:]:
        if maxd<(1-value/np_fund[0:pos].max()):
            maxd=1-value/np_fund[0:pos].max()
            pos=pos+1
    pt_dic['maxd']=maxd

    # volatility
    np_vol=np.log(np_fund[1:])-np.log(np_fund[0:-1])
    pt_dic['volat']=np_vol.std()*np.sqrt(trading_days_per_year)

    # Sharpe Ratio
    pt_dic['sharpe']=(pt_dic['arr']-norisk_ratio)/pt_dic['volat']

    # beta
    cov_mtx=np.cov(np_fund, pt['base'].values)
    pt_dic['beta']=cov_mtx[1,1]/np.var(pt['base'].values)

    # alpha
    pt_dic['alpha']=(pt_dic['arr']-norisk_ratio)-pt_dic['beta']*(pt_dic['barr']-norisk_ratio)


    return pt_dic


#-------------------------------------------------------------------
'''
bias_ratio=cal_nday_bias(pt, nday)
'''
#-------------------------------------------------------------------

def cal_nday_bias(curr_date_obj, pt, nday):
    
    ma_period=datetime.timedelta(days=nday)
    ma_ref=pt.loc[curr_date_obj-ma_period:curr_date_obj].mean()
    bias_ratio = (pt.loc[curr_date_obj]-ma_ref)/ma_ref
    return bias_ratio

 #-------------------------------------------------------------------
'''
unique_id=md5_unique(string)
'''
#-------------------------------------------------------------------

def md5_unique(string):
     md5id=hashlib.md5()
     md5id.update(string.encode('utf-8'))
     return md5id.hexdigest()
 
