#!/usr/bin/env python

"Function call to read dataframe from eq ohlc tables"

import pymysql
import pandas as pd
import os, sys, json, datetime


from dbapi import mc_dbapi
from aes_crypto import AESCipher
from utils import md5_unique
from const import const
'''------------------------

df0       dataframe for the target
    symbol,trading_date,open,high,low,close,volume
'''

def get_us_eq_hist():
    # search bbid
    bbid_dic=mc_dbapi.fetch_bbid('STO')
    print(mc_dbapi.fetch_ohlc(bbid_dic['bbid'],'20180304','20180905'))
        
if __name__=='__main__':
    get_us_eq_hist()
