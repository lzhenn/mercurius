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
    ii=100
    while 1:
        fn='/instrument_%03d.json' % ii
        json_str=open(eq_path+'/'+fn).read()
        json_str=json_str.replace('\\\\\\','xxx')
        json_str=json_str.replace('\\','')
        json_str=json_str.replace('xxx','\\')
        json_str=json_str.strip('"')
        print(json_str[-1])
        data=json.loads(json_str)
        try:
            ii=ii+1
            url=data['next']
            print(url)
            if len(url)<20:
                exit()
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()
            with open(eq_path+'/instrument_%03d.json' % ii, 'w') as f:
                json.dump(response.decode('ascii'), f)
            fn='instrument_%03d.json' % ii
        except:
            print('\nError while downloading %s@%s' % (symb[0], item))
               
        symblist=[]
        sptime=random.randint(100,300)/10
        print('\nsleep %4.2fs' % sptime)
        time.sleep(sptime)
        

if __name__ == '__main__':
    mainfunc()
