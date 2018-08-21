#!/usr/bin/env python

import pymysql
import pandas as pd
import os, sys, json

sys.path.append('../utils')
from aes_crypto import AESCipher
from utils import md5_unique

# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/compliment1808/'
# equity list
#eq_market=['ETF','AMEX','NYSE']




def mainfunc():
    pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
    code =pd_cre.loc['mysql','cred']
    
    crypto_obj=AESCipher('Always Love You')
    passwd=crypto_obj.decrypt(code)
    
    connection = pymysql.connect(host='localhost',
                             user='lzhenn',
                             password=passwd,
                             db='mercuriusdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    files=os.listdir(eq_path)
    pos=0
    
    for item0 in files:  # loop the market
        df=pd.read_csv(eq_path+'/'+item0, parse_dates=True)
        itm_arr=item0.split('.')
        with connection.cursor() as cursor:
            sql = "SELECT bbid FROM `eq_symbol_id_name` WHERE `symbol`=%s"
            cursor.execute(sql, itm_arr[0])
            result = cursor.fetchone()
        if result is None:
            pos=pos+1
            print(itm_arr[0]+' failed!')
            continue
        print(result['bbid']+'-->'+itm_arr[0])
        
        for idx, row in df.iterrows():
            year=row['Date'][0:4]
            mcid=str(md5_unique(itm_arr[0]+row['Date'])) 
            
            with connection.cursor() as cursor:
                sql='CREATE TABLE IF NOT EXISTS eq_symbol_ohlc_'+str(year)+'(symbol varchar(10) NOT NULL,\
                bbid varchar(30) NOT NULL,\
                mcid char(32) NOT NULL primary key,\
                trading_date date NULL,\
                open float  NOT NULL,\
                high float  NOT NULL,\
                low  float  NOT NULL,\
                close float NOT NULL,\
                adj_close  float NULL,\
                volume int NOT NULL,\
                adj_volume int NuLL)'
            
                cursor.execute(sql)
                
                sql = "INSERT INTO `eq_symbol_ohlc_"+str(year)+\
                      "` (`symbol`,`bbid`, `mcid`,`trading_date`, `open`, `high`, `low`, `close`, `adj_close`, `volume`, `adj_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "+\
                      "on duplicate key update `symbol`=`symbol`;"

                cursor.execute(sql, (str(itm_arr[0]),str(result['bbid']),str(mcid),str(row['Date']),str(row['Open']),str(row['High']),str(row['Low']),str(row['Close']),str(row['Adj Close']),str(row['Volume']),str(row['Volume'])))
            connection.commit()

    connection.close()

if __name__=='__main__':
    mainfunc()
