#/usr/bin/env python

"module for download US equity data daily from robinhood private api"

import pandas as pd
import numpy as np
import datetime, time, random
import json
import os
import urllib.request
from bs4 import BeautifulSoup

# equity path
fd_path='/home/lzhenn/array/lzhenn/findata/equity/fundamental'
is_path='/home/lzhenn/array/lzhenn/findata/equity/instrument'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']

def mainfunc():

    files=os.listdir(fd_path)
    sym_id=pd.read_csv(is_path+'/idlist.csv',names=['symb','id'], index_col='id')
    for item in files:
        symb=item.split('-')
        if len(symb)>0:
            print(item)
            json_str=open(fd_path+'/'+item).read()
            json_str=json_str.replace('\\\\\\','xxx')
            json_str=json_str.replace('\\','')
            json_str=json_str.replace('xxx','\\')
            json_str=json_str.strip('"')
            print(json_str)
            #data=json.loads(json_str)
            #datalist=data['results'] 
            #for item in datalist:
            #    print(datalist['instrument'])
            exit()
if __name__ == '__main__':
    mainfunc()
