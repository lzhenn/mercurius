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
    with mc_dbapi.connection.cursor() as cursor:
        sql = "SELECT bbid FROM `eq_symbol_id_name` WHERE `symbol`=%s"
        cursor.execute(sql, "AAPL")
        result = cursor.fetchone()
    if result is None:
        print('failed!')
    else:    
        print(result)
        print(const.MERC_ROOT)
if __name__=='__main__':
    get_us_eq_hist()
