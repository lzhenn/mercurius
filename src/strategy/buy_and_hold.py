#/usr/bin/env python

"Buy and hold strategy, the simplist strategy"

import datetime
import pandas as pd
import numpy as np

'''------------------------

df0       dataframe for the target
tg_name   target name (col name) in df0

    pt['value']    total share value
    pt['share']    total share
    pt['cash']     cash in hand
    pt['trade']    -1 sell; 1 buy; 0 hold
    pt['cost']     average cost

'''
def buy_and_hold(initime_obj, outtime_obj, ini_fund, df0, tg_name, s_ratio):
    
    df_per_share=df0/s_ratio  # timeseries of our target
    ini_price_per_share=df_per_share.loc[initime_obj]
    
    # All in
    max_share = int(ini_fund/ini_price_per_share)
    ini_eq=max_share*ini_price_per_share
    ini_cash=ini_fund-ini_eq
    df_epoch=df_per_share.loc[initime_obj:outtime_obj]

    # build output
    pt = pd.DataFrame(df_epoch.values, index=df_epoch.index, columns=['value'])
    pt['share']=max_share
    pt['cash']=ini_cash
    pt['trade']=0
    pt['cost']=ini_price_per_share
 
    # loop the strategy
    
    # copy data for quick calculation
    pt_matrix=pt.values
    ii=0
    for item in df_epoch:
        pt_matrix[ii,0]= pt_matrix[ii,1]*item
        ii=ii+1
    pt[:]=pt_matrix  
#    pt_dic = strategy_info('buy and hold', pt)
    return pt
