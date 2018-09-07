#coding:utf-8
import pymysql
import pandas as pd
from const import const
from aes_crypto import AESCipher

class _dbapi:

    def __init__(self):
        pd_cre=pd.read_csv(const.MERC_ROOT+'/credential/credential.csv', index_col='item')
        code =pd_cre.loc['mysql','cred']
        crypto_obj=AESCipher('Always Love You')
        passwd=crypto_obj.decrypt(code)
        
        self.connection = pymysql.connect(host='localhost',
                                 user='lzhenn',
                                 password=passwd,
                                 db='mercuriusdb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

mc_dbapi=_dbapi()
