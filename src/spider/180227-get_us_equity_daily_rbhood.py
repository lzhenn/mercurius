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
eq_path='/home/lzhenn/array/lzhenn/findata/equity/'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']

def mainfunc():

    for item in eq_market:
        files=os.listdir(eq_path+item)
        
        pos=0
        symblist=[]
        for item0 in files:
            pos=pos+1
            symb=item0.split('.')
            if symb[1] == 'csv':
                if not(os.path.isfile(eq_path+item+'/'+symb[0]+'_fundamental.json')):
                    symblist.append(symb[0])
                    if len(symblist)==50:
                        symblist_str=",".join(str(symbitem) for symbitem in symblist)
                        print(symblist_str) 
                        try:
                            url='https://api.robinhood.com/fundamentals/?symbols='+symblist_str
                            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.360' }
                            req = urllib.request.Request(url, None, headers)
                            response = urllib.request.urlopen(req).read()
                            print(response)
                            with open(eq_path+item+'/'+symblist[0]+'-'+symblist[-1]+'_fundamental.json', 'w') as f:
                                json.dump(response.decode('ascii'), f)
                        except:
                            print('i\nError while downloading %s@%s' % (symb[0], item))
                            
                        symblist=[]
                        sptime=random.randint(100,300)/10
                        print('\nsleep %4.2fs' % sptime)
                        time.sleep(sptime)
        
        symblist_str=",".join(str(symbitem) for symbitem in symblist)
        print(symblist_str) 
        try:
            url='https://api.robinhood.com/fundamentals/?symbols='+symblist_str
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.360' }
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()
            print(response)
            with open(eq_path+item+'/'+symblist[0]+'-'+symblist[-1]+'_fundamental.json', 'w') as f:
                json.dump(response.decode('ascii'), f)
        except:
            print('i\nError while downloading %s@%s' % (symb[0], item))

if __name__ == '__main__':
    mainfunc()
