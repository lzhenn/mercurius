#/usr/bin/env python

"Up in down out strategy, trend follower"

import datetime
import pandas as pd
import numpy as np

'''------------------------

df0       dataframe for the target
tg_name   target name (col name) in df0

 mtx[0]    pt['value']    total share value
 mtx[1]   pt['share']    total share
 mtx[2]   pt['cash']     cash in hand
 mtx[3]   pt['trade']    -1 sell; 1 buy; 0 hold
 mtx[4]   pt['cost']     average cost

'''
def up_in_down_out(initime_obj, outtime_obj, ini_fund, df0, tg_name, s_ratio):
    
    # parameters
    ma_period=datetime.timedelta(days=365)


    df_per_share=df0/s_ratio                            # target adjestment 
    ini_price_per_share=df_per_share.loc[initime_obj]   # initial price
    df_epoch=df_per_share.loc[initime_obj:outtime_obj]  # timeseries of our target


    # build output
    pt = pd.DataFrame(np.zeros(len(df_epoch.values)), index=df_epoch.index, columns=['value'])
    pt['share']=0
    pt['cash']=ini_fund
    pt['trade']=0
    pt['cost']=0
 
    # loop the strategy
    
    # copy data for quick calculation
    pt_matrix=pt.values
    ii=0
    for item in df_epoch:
        date_now=df_epoch.index[ii]
        ma_ref=df_epoch.loc[date_now-ma_period:date_now].mean()
        if (item >= ma_ref) and (ii>0):   # current price > MA indicator
            if pt_matrix[ii-1,1] == 0:    # empty position
                # All in
                max_share = int(pt_matrix[ii-1,2]/item)
                pt_matrix[ii,0] = max_share*item
                pt_matrix[ii,1] = max_share
                pt_matrix[ii,2] = pt_matrix[ii-1,2]-max_share*item
                pt_matrix[ii,3] = 1
                pt_matrix[ii,4] = item
            else:
                # Hold
                pt_matrix[ii,1] = pt_matrix[ii-1,1]
                pt_matrix[ii,0] = pt_matrix[ii,1]*item
                pt_matrix[ii,2] = pt_matrix[ii-1,2]
                pt_matrix[ii,3] = 0
                pt_matrix[ii,4] = pt_matrix[ii-1,4]
                
        elif (item < ma_ref) and (ii>0):
            if (pt_matrix[ii-1,1] == 0):    # empty position
                pt_matrix[ii,2] = pt_matrix[ii-1,2]
            else:
                # All out
                pt_matrix[ii,0] = 0
                pt_matrix[ii,1] = 0
                pt_matrix[ii,2] = pt_matrix[ii-1,2]+pt_matrix[ii-1,1]*item
                pt_matrix[ii,3] = -1
                pt_matrix[ii,4] = 0
        ii=ii+1
    pt[:]=pt_matrix   
    pbase=buy_and_hold(initime_obj, outtime_obj, ini_fund, df0, tg_name, s_ratio)
    pt['base']=pbase['base']
    return pt
