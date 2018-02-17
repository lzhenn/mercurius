#/usr/bin/env python

"ensemble hindcast for single strategy"

'''
    hindcast start time =========================================> hindcast end time
                            |------->
                            *****|------->
                                 *****|------->  
                             
                             
                                                    ********  ensemble granularity  
                                                    |------>  invest period                                
'''



import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../strategy')
sys.path.append('../utils')

from buy_and_hold import buy_and_hold as strategy
#from up_in_down_out import up_in_down_out as strategy
#from grid_trading import grid_trading as strategy
from utils import parse_trading_day, parse_trading_day_foreward, cal_nday_bias


# data path
dpath='/home/lzhenn/array/lzhenn/findata/commodities/'

# speculate/investment target
target='GOLD-LBMA'
target_colname='USD (AM)'

# hindcast start time
initime_str='1991-01-01'

# hindcast end time
endtime_str='2018-01-24'

# invest period
invest_p=60

# invest ensemble granularity, if = 7, means every 7 trading day per ensemble start
gran_p = 1

# initial fund
ini_fund=10000

# share ratio
r_share=1358/128.83


int_time_obj = datetime.datetime.strptime(initime_str, '%Y-%m-%d')
end_time_obj = datetime.datetime.strptime(endtime_str, '%Y-%m-%d')

def mainfunc():
    with open(dpath+target, 'r') as f:
        df=pd.read_csv(f, index_col='Date', parse_dates=True)
    df0=df[target_colname]
    int_time_obj_new = parse_trading_day(df0.index, int_time_obj)   # get hindcast day start
    end_time_obj_new = parse_trading_day(df0.index, end_time_obj)   # get hindcast day end
    invest_time_delta=datetime.timedelta(days=invest_p)
    esm_time_delta=datetime.timedelta(days=gran_p)

    print("Ensemble Hindcast Start: "+int_time_obj_new.strftime('%y-%m-%d'))
    print("Ensemble Hindcast End: "+end_time_obj_new.strftime('%y-%m-%d'))

    curr_start_time_obj = int_time_obj_new                              # ensemble member start
    curr_end_time_obj = parse_trading_day(df0.index,curr_start_time_obj+invest_time_delta) # ensemble member end
    n_esm=0
    while (curr_end_time_obj < end_time_obj_new ):
        n_esm = n_esm+1
        print('Ensemble Member %5d Start: %s' % (n_esm,curr_start_time_obj.strftime('%y-%m-%d')))
        print('Ensemble Member %5d End: %s' % (n_esm,curr_end_time_obj.strftime('%y-%m-%d')))
        bias_r = cal_nday_bias(curr_start_time_obj, df0, 50)
        print(bias_r)
        info_dic, fund_pd=strategy(curr_start_time_obj, curr_end_time_obj, ini_fund, df0, target_colname, r_share)
        # Shift one ensemble granularity foreward
        curr_start_time_obj = parse_trading_day_foreward(df0.index, curr_start_time_obj+esm_time_delta)
        curr_end_time_obj = parse_trading_day_foreward(df0.index, curr_end_time_obj+esm_time_delta)
        plt.plot(bias_r, info_dic['arr'],'.', color='blue')
    plt.title('Bias Return Relation')
    plt.show()
    

if __name__ == '__main__':
    mainfunc()
