#!/usr/bin/env python

import pandas as pd
import pymysql
import os, sys, hashlib
sys.path.append('../utils')
from aes_crypto import AESCipher


# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/financials/'
   
dbname='mercuriusdb'

def mainfunc():
    
    # Read the password 
    pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
    code =pd_cre.loc['mysql','cred']
    crypto_obj=AESCipher('Always Love You')
    passwd=crypto_obj.decrypt(code)
   
    # connect database
    connection= pymysql.connect(host='localhost',
                             user='lzhenn',
                             password=passwd,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


    pos=0
    files=os.listdir(eq_path)
    for item0 in files:

        itm_arr=item0.split('_')
        itm_symbol=itm_arr[0]
        itm_fin=itm_arr[1]
        if itm_fin == 'Balance%20Sheet.xlsx':
            print('Deal with '+item0)
            file_path=eq_path+item0
            # Deal with the financial record
            df=pd.read_excel(file_path)
            df=df.T//1000   # Change the unit to kdollars 
            with connection.cursor() as cursor:
                sql = "SELECT `rhid` FROM `eq_all_basics` WHERE `symbol`=%s"
                cursor.execute(sql, itm_symbol)
                result = cursor.fetchone()
                if result is None:
                    pos=pos+1
                    print(str(pos)+' failed!')
                    continue
                sql = "INSERT INTO `eq_balance_sheet` (`rhid`, `symbol`, `issued_date`, `cash_equiv`,`invest_curr`, `cash_st_invest`, `receivables`, `inventory`, `curr_ast`, `ppe_net`, `goodwill`, `invst_ncurr`, `tax_ast`, `ast_ncurr`, `total_ast`, `payables`, `debt_curr`, `curr_liab`, `debt_ncurr`, `total_debt`, `def_revenue`, `tax_liab`, `dep_liab`, `liab_ncurr`, `total_liab`, `other_income`, `ret_earning`, `equity`, `invest`, `md5id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
                
    
                for idx, df_itm in df.iterrows():
                    data_stream=[result['rhid'], itm_symbol, idx.strftime('%Y-%m-%d %H:%M:%S')]
                    data_stream.extend(df_itm.tolist())            
                    md5id=hashlib.md5()
                    md5id.update((itm_symbol+idx.strftime('%Y-%m-%d %H:%M:%S')).encode('utf-8'))
                    data_stream.append(md5id.hexdigest())
                    try:
                        cursor.execute(sql, tuple(data_stream))
                    except:
                        continue
        
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    connection.close()


if __name__=='__main__':
    mainfunc()
