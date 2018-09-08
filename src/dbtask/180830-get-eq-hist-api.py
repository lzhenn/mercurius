#!/usr/bin/env python

"Function call to read dataframe from eq ohlc tables"

import pymysql
import pandas as pd
import os, sys, json, datetime

merc_root='/home/lzhenn/workspace/mercurius'

sys.path.append(merc_root+'/src/utils')
from aes_crypto import AESCipher
from utils import md5_unique

'''------------------------

df0       dataframe for the target
    symbol,trading_date,open,high,low,close,volume
'''

def get_us_eq_hist_api(initime_obj, outtime_obj, symbol):


    end_year=outtime_obj.year
    strt_year=initime_obj.year
    
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
     # search bbid
    with connection.cursor() as cursor:
        sql = "SELECT bbid FROM `eq_symbol_id_name` WHERE `symbol`=%s"
        cursor.execute(sql, symbol)
        result = cursor.fetchone()
    if result is None:
        print('failed!')
    else:    
        sql = "SELECT symbol FROM `eq_symbol_id_name` WHERE `bbid`=%s"
        cursor.execute(sql, result)
        result_all = cursor.fetchone()

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
