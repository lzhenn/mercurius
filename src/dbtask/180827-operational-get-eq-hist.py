#!/usr/bin/env python

import pymysql
import pandas as pd
import os, sys, json, datetime

merc_root='/home/lzhenn/workspace/mercurius'

sys.path.append(merc_root+'/src/utils')
from aes_crypto import AESCipher
from utils import md5_unique

def mainfunc():


    date_lastday=datetime.datetime.now()+datetime.timedelta(days=-1)
    date_year=date_lastday.year
    
    
    pd_cre=pd.read_csv(merc_root+'/credential/credential.csv', index_col='item')
    code =pd_cre.loc['mysql','cred']
    
    crypto_obj=AESCipher('Always Love You')
    passwd=crypto_obj.decrypt(code)
    
    connection = pymysql.connect(host='localhost',
                             user='lzhenn',
                             password=passwd,
                             db='mercuriusdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    # initial read

    sql = "SELECT symbol,trading_date,open,high,low,close,volume FROM `eq_symbol_ohlc_"+str(date_year-10)+"` WHERE `symbol`='AAPL'"
    df=pd.read_sql(sql, con=connection)
    
    for yy in range(date_year-9,date_year+1):
        sql = "SELECT symbol,trading_date,open,high,low,close,volume FROM `eq_symbol_ohlc_"+str(yy)+"` WHERE `symbol`='AAPL'"
        df_temp=pd.read_sql(sql, con=connection)
        df=df.append(df_temp, ignore_index=True)
    connection.close()
    print(df)
if __name__=='__main__':
    mainfunc()
