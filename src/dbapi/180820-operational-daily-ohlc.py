#!/usr/bin/env python

import pymysql
import pandas as pd
import os, sys, json, datetime

merc_root='/home/lzhenn/workspace/mercurius'

sys.path.append(merc_root+'/src/utils')
from aes_crypto import AESCipher
from utils import md5_unique

date_lastday=datetime.datetime.now()+datetime.timedelta(days=-1)
date_str=date_lastday.strftime('%Y%m%d')
datapath='/home/lzhenn/array/lzhenn/findata-daily/raw/market_'+date_str+'.json'

def mainfunc():
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
    
    json_str=open(datapath).read()
    json_str=json_str.replace('\\','')
    json_str=json_str.strip('"')
    data=json.loads(json_str)
    pos=0
    for item in data:   # loop the data
        with connection.cursor() as cursor:
            sql = "SELECT bbid FROM `eq_symbol_id_name` WHERE `symbol`=%s"
            cursor.execute(sql, data[item]['symbol'])
            result = cursor.fetchone()
            if result is None:
                pos=pos+1
                print(data[item]['symbol']+' failed!')
                continue
            print(result['bbid']+'-->'+data[item]['symbol'])
        year=data[item]['date'][0:4]
        mcid=str(md5_unique(data[item]['symbol']+data[item]['date'])) 
        
        try: # test the existence of variables
            data[item]['open']
            data[item]['high']
            data[item]['low']
            data[item]['close']
            data[item]['volume']
            data[item]['unadjustedVolume']
        except:
            print(data[item]['symbol']+' variable not found!!!')
            continue

        with connection.cursor() as cursor: # create the table is not exist
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

            cursor.execute(sql, (str(data[item]['symbol']),str(result['bbid']),str(mcid),str(data[item]['date']),str(data[item]['open']),str(data[item]['high']),str(data[item]['low']),str(data[item]['close']),str(data[item]['close']),str(data[item]['unadjustedVolume']),str(data[item]['volume'])))
        # end with 
        connection.commit()
    # end for data loop
    connection.close()

if __name__=='__main__':
    mainfunc()
