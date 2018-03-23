#!/usr/bin/env python

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os, sys, json
sys.path.append('../utils')
from aes_crypto import AESCipher


# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/'
# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']



def mainfunc():
    pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
    code =pd_cre.loc['mysql','cred']
    crypto_obj=AESCipher('Always Love You')
    passwd=crypto_obj.decrypt(code)
    

    dbname='mercuriusdb'

    connection = create_engine("mysql+pymysql://lzhenn:"+passwd+"@localhost/"+dbname)

    connection2 = pymysql.connect(host='localhost',
                             user='lzhenn',
                             password=passwd,
                             db='mercuriusdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    for item in eq_market:
        files=os.listdir(eq_path+item)
        
        pos=0
        for item0 in files:
            df=pd.read_csv(eq_path+item+'/'+item0, parse_dates=True)
            itm_arr=item0.split('.')
            with connection2.cursor() as cursor:
                sql = "SELECT bbid FROM `eq_all_basics` WHERE `symbol`=%s"
                cursor.execute(sql, itm_arr[0])
                result = cursor.fetchone()
                if result is None:
                    pos=pos+1
                    print(str(pos)+' failed!')
                    continue
                print(result['bbid']+'-->'+itm_arr[0])
                try:
                    sql='DROP TABLE '+result['bbid']
                    cursor.execute(sql)
                except:
                    continue
                # Create a new record
            #df.to_sql(name=result['bbid'], con=connection, if_exists = 'replace', index=False)
            #cursor.executemany(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection2.commit()
    connection2.close()

if __name__=='__main__':
    mainfunc()
