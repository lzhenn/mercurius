
#coding:utf-8
#/usr/bin/env python

"""Class Portfolio 

This class is the motherboard for any portfolio management strategy. 

"""

import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from const import const
import sys

sys.path.append(const.MERC_ROOT+'/src/strategy')
class portfolio_pkg(object):
    """
    Args:
        * target_names (str): name list of the targeted object
        * data_start_date (str): data start date
        * strategy_start_time (str): yyyymmdd strategy start date
        * strategy_end_time (str): yyyymmdd strategy end date
        * pos_adj_cycle (int): days per cycle to adjust the position
        * ini_fund (float): initial fund to invest in the target
        * alloc_method (str): 'risk parity', 'equal', 'maximum spread'
        * timing_strategy (str): 'buy and hold', 'up in down out'
    """
    def __init__(self,target_names, data_start_date, strategy_start_time, strategy_end_time, pos_adj_cycle, init_fund=100000.0, alloc_method='risk parity', timing_strategy='up in down out'):
        
        self.target_names=target_names
        self.pos_adj_cycle=pos_adj_cycle
        self.init_fund=init_fund
        self.data_start_date=data_start_date
        self.strategy_start_time=strategy_start_time
        self.strategy_end_time=strategy_end_time
        self.alloc_method=alloc_method
        self.timing_strategy=timing_strategy

        self.obj_data_date0=datetime.datetime.strptime(data_start_date,'%Y%m%d')
        self.obj_date0=datetime.datetime.strptime(strategy_start_time,'%Y%m%d')
        self.obj_date1=datetime.datetime.strptime(strategy_end_time,'%Y%m%d')
        
        self.load_data()
        self.allocate_position()
        print('Portfolio Object Initialized!')

    def load_data(self):
        from dbapi import mc_dbapi
        self.df=pd.DataFrame()
        for tgt in self.target_names:
            print(tgt+' loading...')
            bbid_dic=mc_dbapi.fetch_bbid(tgt)
            df=mc_dbapi.fetch_ohlc(bbid_dic['bbid'],self.data_start_date,self.strategy_end_time)
            df=df.loc[:,['middle']]
            df=df.rename(columns={"middle":tgt} )
            self.df=pd.concat([self.df, df], axis=1)

    def allocate_position(self):
        
        self.info={}
        alloc_ratio=0.0
        if self.alloc_method=='risk parity':
            for tgt in self.target_names:
                # calculate volatility
                np_vol=np.log(self.df[tgt].values[1:])-np.log(self.df[tgt].values[0:-1])
                self.info[tgt]={}
                self.info[tgt]['std']=np_vol.std()
                alloc_ratio=alloc_ratio+1.0/self.info[tgt]['std']
            alloc_ratio=1.0/alloc_ratio

            for tgt in self.target_names:
                self.info[tgt]['alloc']=alloc_ratio/self.info[tgt]['std']
        elif self.alloc_method=='equal':
            n_tgt=len(self.target_names)
            for tgt in self.target_names:
                self.info[tgt]['alloc']=1.0/n_tgt


    def drive_timing_strategy(self):
        from utils import parse_trading_day
        if self.timing_strategy == 'up in down out':
            from up_in_down_out import up_in_down_out as strategy
        elif self.timing_strategy == 'buy and hold':
            from buy_and_hold import buy_and_hold as strategy

        self.obj_date0=parse_trading_day(self.df.index, self.obj_date0)
        #self.obj_date1=parse_trading_day(self.df.index, self.obj_date1) # end date
       
        # Initialize the first adjustment cycle
        adj_date_obj0=self.obj_date0
        adj_date_obj1=adj_date_obj0+datetime.timedelta(days=self.pos_adj_cycle)
        adj_date_obj1=parse_trading_day(self.df.index,adj_date_obj1)
        adj_total_fund=self.init_fund
        
        self.df['total_cash']=0.0
        self.df['total_eq']=0.0
        self.df['interest']=0.0
        self.df['total_value']=0.0
        
        for tgt in self.target_names:
            self.info[tgt]['fundflow']=pd.DataFrame()
        
        while adj_date_obj1 < self.obj_date1:  # till end time
            
            for tgt in self.target_names:
                df=strategy(adj_date_obj0, adj_date_obj1, adj_total_fund*self.info[tgt]['alloc'], self.df.loc[:adj_date_obj1,[tgt]], 1.0)
                self.info[tgt]['fundflow']=self.info[tgt]['fundflow'].append(df)
                self.adjust_position()
            
            self.get_portfolio_track()
            
            adj_date_obj0=adj_date_obj1
            adj_date_obj1=adj_date_obj1+datetime.timedelta(days=self.pos_adj_cycle)
            adj_date_obj1=parse_trading_day(self.df.index,adj_date_obj1)
    
    def adjust_position(self):
        pass 
    
    def get_portfolio_track(self):
        
        """
        Return the portfolio attributes
        
        Returns:
            * self.df (DataFrame): original dataframe plus the following columns
                total_cash (float): total cash in hand
                total_eq (float): total value of equity in hand
                interest (float): interest paid to the portfolio cash
                total_value (float): total_cash + total_eq + interest
        """
        
        from const import const
        from utils import parse_trading_day
        
        
        #---------- prepare --------------
        norisk_ratio=const.NO_RISK_RETURN
        trading_days_per_year=const.TRAD_DAYS_PER_YEAR
        for tgt in self.target_names:
            self.df['total_cash']=self.df['total_cash']+self.info[tgt]['fundflow']['cash']      
            self.df['total_eq']=self.df['total_eq']+self.info[tgt]['fundflow']['value']      
            self.df['interest']=((norisk_ratio+1)**(1.0/trading_days_per_year)-1)*self.df['total_cash']
            self.df['total_value']=self.df['total_cash'].values+self.df['total_eq'].values+np.add.accumulate(np.nan_to_num(self.df['interest'].values))



             
    def plot_funding_curve(self):
        ax = plt.subplot(111)
        plt.plot(self.reffundflow['value']+self.reffundflow['cash'], '-', color='gray', alpha=0.8, label='Buy & Hold')
        plt.title(self.target_name+' Funding curve')
        plt.plot(self.fundflow['value']+self.fundflow['cash'], '-', color='blue', label=self.strategy_name)
        buy_point=(self.fundflow['value']+self.fundflow['cash'])*self.fundflow['trade']
        buy_point=buy_point[buy_point>0]
        plt.plot(buy_point, 'o', color='darkgreen', alpha=0.8, label='buy point')
        sell_point=(self.fundflow['value']+self.fundflow['cash'])*self.fundflow['trade']
        sell_point=sell_point[sell_point<0]
        sell_point=-sell_point
        plt.plot(sell_point, 'o', color='red', alpha=0.8, label='sell point')
        plt.grid(True)
        plt.legend(loc='best', ncol=2 )
        #plt.show()

