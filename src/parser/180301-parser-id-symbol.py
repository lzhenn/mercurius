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
eq_path='/home/lzhenn/array/lzhenn/findata/equity/instrument'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']

def mainfunc():

    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.360' }
    ii=0
    csvf=open(eq_path+'/idlist.csv','w')
    while 1:
        fn='instrument_%03d.json' % ii
        print(fn)
        json_str=open(eq_path+'/'+fn).read()
        json_str=json_str.replace('\\\\\\','xxx')
        json_str=json_str.replace('\\','')
        json_str=json_str.replace('xxx','\\')
        json_str=json_str.strip('"')
        data=json.loads(json_str)
        datalist=data['results'] 
        for item in datalist:
            csvf.write(item['symbol']+','+item['id']+'\n')
        ii=ii+1
if __name__ == '__main__':
    mainfunc()
