#/usr/bin/env python

"module for download US equity data that download unsuccessfully"

import pandas as pd
import numpy as np
import datetime 
import yahoo_finance
import fix_yahoo_finance as yf
import time
import random
import os
from pandas_datareader import data as pdr


# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/'
eq_com_path=eq_path+'compliment/'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']


ini_time='2018-02-02'
end_time='2018-02-28'

int_time_obj = datetime.datetime.strptime(ini_time, '%Y-%m-%d')
end_time_obj = datetime.datetime.strptime(end_time, '%Y-%m-%d')

def mainfunc():

    yf.pdr_override() # fix yahoo finance api

    files=os.listdir(eq_com_path)
    
    pos=0
    for item0 in files:
        pos=pos+1
        fsize = os.path.getsize(eq_com_path+item0)
        print('%s with size:%8d:' % (item0,fsize))
        
        if fsize < 100:
            symb=item0.split('.')
            print('\n\nNow download %s@%s (%d)' % (symb[0], item0, pos))
            try:
                df = pdr.get_data_yahoo(symb[0].strip(), start=ini_time, end=end_time)
            except:
                print('\nError while downloading %s@%s' % (symb[0], item0))

            with open(eq_com_path+symb[0].strip()+'.csv', 'w') as f:
                df.to_csv(f)
            
            fsize = os.path.getsize(eq_com_path+item0)
            print('\n%s downloaded! With size:%8d:' % (item0,fsize))
            
            sptime=random.randint(100,300)/10
            print('\nsleep %4.2fs' % sptime)
            time.sleep(sptime)

if __name__ == '__main__':
    mainfunc()
