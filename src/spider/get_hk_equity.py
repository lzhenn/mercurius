#/usr/bin/env python

"module for download US equity data"

import pandas as pd
import numpy as np
import datetime 
import yahoo_finance
import fix_yahoo_finance as yf
import time
import random
from pandas_datareader import data as pdr


# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']

ini_time='1900-01-01'
end_time='2018-02-02'

def mainfunc():
    yf.pdr_override() # fix yahoo finance api
    df = pdr.get_data_yahoo('0700.HK', start=ini_time, end=end_time)
    print(df)


if __name__ == '__main__':
    mainfunc()
