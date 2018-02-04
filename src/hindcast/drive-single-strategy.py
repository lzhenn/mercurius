#/usr/bin/env python

"Buy and hold strategy, the simplist strategy"

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../strategy')
sys.path.append('../utils')

#from buy_and_hold import buy_and_hold as strategy
#from up_in_down_out import up_in_down_out as strategy
from grid_trading import grid_trading as strategy
from utils import parse_trading_day


# data path
dpath='/home/lzhenn/array/lzhenn/findata/commodities/'

# speculate/investment target
target='GOLD-LBMA'
target_colname='USD (AM)'

# start time
initime_str='2011-01-01'

# end time
endtime_str='2018-01-24'

# invest period (optional)
invest_p=6

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
    int_time_obj_new = parse_trading_day(df0.index, int_time_obj)
    end_time_obj_new = parse_trading_day(df0.index, end_time_obj)
    print("Trading Start: "+int_time_obj_new.strftime('%y-%m-%d'))
    print("Trading End: "+end_time_obj_new.strftime('%y-%m-%d'))
    info_dic, fund_pd=strategy(int_time_obj_new, end_time_obj_new, ini_fund, df0, target_colname, r_share)

    print(info_dic)

    plt.plot(fund_pd['value']+fund_pd['cash'])
    buy_point=(fund_pd['value']+fund_pd['cash'])*fund_pd['trade']
    buy_point=buy_point[buy_point>0]
    plt.plot(buy_point, 'o', mfc='red')

    sell_point=(fund_pd['value']+fund_pd['cash'])*(-1)*fund_pd['trade']
    sell_point=sell_point[sell_point>0]
    plt.plot(sell_point, 'o', mfc='blue')
 
    plt.title('Funding curve')
    plt.show()
    

if __name__ == '__main__':
    mainfunc()
