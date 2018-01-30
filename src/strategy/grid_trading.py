#/usr/bin/env python

"Grid trading strategy"

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
def grid_trading(initime_obj, outtime_obj, ini_fund, df0, tg_name, s_ratio):
    
    # parameters
    # rebalance_period=datetime.timedelta(days=30)
    down_grid, down_grid0=0.05, 0.05
    up_grid, up_grid0=0.05, 0.05
    first_pos_ratio=0.5 
    grid_pos_ratio=0.1 # reserved portion


    df_per_share=df0/s_ratio                            # target adjestment 
    ini_price_per_share=df_per_share.loc[initime_obj]   # initial price
    df_epoch=df_per_share.loc[initime_obj:outtime_obj]  # timeseries of our target


    # build output
    pt = pd.DataFrame(np.zeros(len(df_epoch.values)), index=df_epoch.index, columns=['value'])
    pt['share']=0
    pt['cash']=ini_fund
    pt['trade']=0
    pt['cost']=0
    
    # first position
    max_share = int(ini_fund*first_pos_ratio/ini_price_per_share)
    pt.loc[pt.index[0], 'value']=max_share*ini_price_per_share
    pt.loc[pt.index[0], 'share']=max_share
    pt.loc[pt.index[0],'cash']=ini_fund-max_share*ini_price_per_share
    pt.loc[pt.index[0],'trade']=1
    pt.loc[pt.index[0],'cost']=ini_price_per_share
 
    # loop the strategy
    
    # copy data for quick calculation
    pt_matrix=pt.values
    ii=0
    grid_count=0    # how many times have the grids executed
    for item in df_epoch:

        # already done
        if ii==0:
            ii=1
            continue
        
        hold_flag=True    

        date_now=df_epoch.index[ii]
        grid_ref=1-item/pt_matrix[ii-1,4] # price down percent
        if (grid_ref>= down_grid): # need grid in
            if pt_matrix[ii-1,2]>grid_pos_ratio*ini_fund:    # cash in hand > 1 grid requirement
                hold_flag=False
                # one grid in 
                grid_count=grid_count+1
                max_share = int(grid_pos_ratio*ini_fund/item)
                pt_matrix[ii,0] = pt_matrix[ii-1,0]+max_share*item
                pt_matrix[ii,1] = max_share+pt_matrix[ii-1,1]
                pt_matrix[ii,2] = pt_matrix[ii-1,2]-max_share*item
                pt_matrix[ii,3] = 1
                pt_matrix[ii,4] = (pt_matrix[ii-1,4]*pt_matrix[ii-1,1]+item*max_share)/pt_matrix[ii,1]
                down_grid=down_grid+down_grid0
                up_grid=up_grid0
        elif ((-1)*grid_ref >= up_grid) and (grid_count>0): # need grid out
            hold_flag=False
            grid_count= grid_count-1
            # grid out
            max_share = int(pt_matrix[ii-1,1]*grid_pos_ratio)
            pt_matrix[ii,0] = pt_matrix[ii-1,0]-max_share*item
            pt_matrix[ii,1] = pt_matrix[ii-1,1]-max_share
            pt_matrix[ii,2] = pt_matrix[ii-1,2]+max_share*item
            pt_matrix[ii,3] = -1
            pt_matrix[ii,4] = pt_matrix[ii-1,4]
            up_grid=up_grid+up_grid0
            down_grid=down_grid0
        # Hold
        if hold_flag:
            pt_matrix[ii,1] = pt_matrix[ii-1,1]
            pt_matrix[ii,0] = pt_matrix[ii-1,1]*item
            pt_matrix[ii,2] = pt_matrix[ii-1,2]
            pt_matrix[ii,3] = 0
            pt_matrix[ii,4] = pt_matrix[ii-1,4]
        ii=ii+1
    pt[:]=pt_matrix  
    
  #  dic=strategy_info('grid trading', pt)

    return pt
