#/usr/bin/env python

"module for download US equity data"

import pandas as pd
import numpy as np
import datetime 
import yahoo_finance
import yfinance as yf
import time
import random
from pandas_datareader import data as pdr


# equity path
eq_path='/disk/hq247/yhuangci/lzhenn/findata/equity/'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']

ini_time='1949-01-01'
end_time='2019-10-04'

int_time_obj = datetime.datetime.strptime(ini_time, '%Y-%m-%d')
end_time_obj = datetime.datetime.strptime(end_time, '%Y-%m-%d')

def mainfunc():

    yf.pdr_override() # fix yahoo finance api

    for item in eq_market:
        pd_symbol=pd.read_csv(eq_path+item+'.csv', index_col='Symbol')
        pos=0
        for symb in pd_symbol.index:
            pos=pos+1
            print('Now download %s@%s (%d/%d)' % (symb, item, pos, len(pd_symbol.index)))
            try:
                df = pdr.get_data_yahoo(symb, start=ini_time, end=end_time)
            except:
                print('i\nError while downloading %s@%s' % (symb, item))

            with open(eq_path+item+'/'+symb+'.csv', 'w') as f:
                df.to_csv(f)
            sptime=random.randint(0,50)/10
            print('\nsleep %4.2fs' % sptime)
            time.sleep(sptime)

if __name__ == '__main__':
    mainfunc()
