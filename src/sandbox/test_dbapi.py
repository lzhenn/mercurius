#!/usr/bin/env python

import pymysql
import pandas as pd
import sys

sys.path.append('../utils')
from aes_crypto import AESCipher
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
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `eq_all_basics` (`name`, `symbol`, `bbid`, `rhid`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, ('org','OO', 'dfjojfofcd', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()
if __name__=='__main__':
    mainfunc()
