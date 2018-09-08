#coding:utf-8
"""
DBAPI for the mercurius system, initilize, fetch data, and elegently exit.
"""

import pymysql, datetime
import pandas as pd
from const import const
from aes_crypto import AESCipher

class _dbapi:
    def __init__(self):
        """Initilize the dbapi for the mercuriusdb
            dbapi object named as mc_dbapi
        
        Args: self

        Returns: None

        """
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

    def fetch_bbid(self, symbol):
        """Fetch bbid from table `eq_symbol_id_name`
        
            Args: self. symbol

            Returns (dic): bbid 
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT bbid FROM `eq_symbol_id_name` WHERE `symbol`=%s"
            cursor.execute(sql, symbol)
            result = cursor.fetchone()
        if result is None:
            result='failed!'
        
        return result
            
    def fetch_ohlc(self, bbid, start_date, end_date):
        """Fetch OHLC and volume from eq_symbol_YYYY 
        
            Args: self. bbid, start_date, end_date

            Returns (pandas dataframe):
                    df0       dataframe for the target
                    symbol,trading_date,open,high,low,close,volume
        """
        ini_time_obj = datetime.datetime.strptime(start_date,'%Y%m%d')
        end_time_obj = datetime.datetime.strptime(end_date, '%Y%m%d')
        
        end_year=end_time_obj.year
        strt_year=ini_time_obj.year
        
        # initial read
        sql = "SELECT symbol,trading_date,open,high,low,close,volume FROM `eq_symbol_ohlc_"+str(strt_year)+"` WHERE `bbid`='"+bbid+"'"
        df=pd.read_sql(sql, con=self.connection)
    
        for yy in range(strt_year+1,end_year+1):
            sql = "SELECT symbol,trading_date,open,high,low,close,volume FROM `eq_symbol_ohlc_"+str(yy)+"` WHERE `bbid`='"+bbid+"'"
            df_temp=pd.read_sql(sql, con=self.connection)
            df=df.append(df_temp, ignore_index=True)

        # extract desired frames
        df['trading_date']=pd.to_datetime(df['trading_date'])
        df=df.set_index('trading_date')
        return df.loc[start_date:end_date]

mc_dbapi=_dbapi()
