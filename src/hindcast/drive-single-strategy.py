#/usr/bin/env python

"Buy and hold strategy, the simplist strategy"

import datetime
import pandas as pd
import numpy as np
import sys
sys.path.append('../strategy')
from buy_and_hold import buy_and_hold as strategy

# data path
dpath='/home/lzhenn/array/lzhenn/findata/commodities/'

# speculate/investment target
target='GOLD-LBMA'
target_colname='USD (AM)'

# start time
initime_str='2016-07-22'

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
    fund_pd=strategy(int_time_obj, end_time_obj, ini_fund, df0, target_colname, r_share)
    print(fund_pd)

if __name__ == '__main__':
    mainfunc()
