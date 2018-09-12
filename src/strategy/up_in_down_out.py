#/usr/bin/env python

"Up in down out strategy, trend follower"

import datetime
import pandas as pd
import numpy as np

'''------------------------

df0       dataframe for the target

 mtx[0]    pt['value']    total share value
 mtx[1]   pt['share']    total share
 mtx[2]   pt['cash']     cash in hand
 mtx[3]   pt['trade']    -1 sell; 1 buy; 0 hold/empty
 mtx[4]   pt['cost']     average cost

'''
def up_in_down_out(initime_obj, outtime_obj, ini_fund, df0, s_ratio):
    
    """
    Args:
        * initime_obj (datetime.datetime): initial time obj for driving the strategy
        * outtime_obj (datetime.datetime): final time obj for driving the strategy
        * ini_fund (float): initial fund
        * df0 (pandas.dataframe): price timeseries of the atarget
        * s_ratio (float): folding ratio between the object and the target. for example, 
        the gold price is 1322$/oz. However, the target is GLD, and the GLD price is
        123$/share, therefore. s_ratio=1322/123. Typically, s_ratio=1.0
    """
    df0.columns=['value']
    # parameters
    ma_period=datetime.timedelta(days=-365)


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
    for item in df_epoch['value']:
        date_now=df_epoch.index[ii]
        ma_ref=df_per_share.loc[date_now+ma_period:date_now]['value'].mean()
        if (item >= ma_ref):   # current price > MA indicator
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
                
        elif (item < ma_ref):
            if (pt_matrix[ii-1,1] == 0):    # empty position
                pt_matrix[ii,2] = pt_matrix[ii-1,2]
                pt_matrix[ii,3] = 0
                pt_matrix[ii,4] = pt_matrix[ii-1,4]
            else:
                # All out
                pt_matrix[ii,0] = 0
                pt_matrix[ii,1] = 0
                pt_matrix[ii,2] = pt_matrix[ii-1,2]+pt_matrix[ii-1,1]*item
                pt_matrix[ii,3] = -1
                pt_matrix[ii,4] = pt_matrix[ii-1,4]
        elif (ii>0):
            # Hold
            pt_matrix[ii,1] = pt_matrix[ii-1,1]
            pt_matrix[ii,0] = pt_matrix[ii,1]*item
            pt_matrix[ii,2] = pt_matrix[ii-1,2]
            pt_matrix[ii,3] = 0
            pt_matrix[ii,4] = pt_matrix[ii-1,4]

        ii=ii+1
    pt[:]=pt_matrix   
    return pt
