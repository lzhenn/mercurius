
#coding:utf-8
#/usr/bin/env python

"""Class Strategy

This class is the motherboard for any hindcastable strategy. 

"""

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../strategy')

class strategy_pkg(object):
    """
    Args:
        * target_name (str): name of the targeted object
        * df (pandas dataframe): dataframe of the target historical values
            df sample:
                TIMESTAMP     VALUE
                2018-08-29    112.5  
                2018-08-30    113.1
        * ini_fund (float): initial fund to invest in the target
    """
    def __init__(self,target_name, df, strategy_start_time, strategy_end_time, init_fund=10000.0):
        
        self.target_name=target_name
        self.init_fund=init_fund
        self.data_start_time=df.index[0]
        self.data_end_time=df.index[-1]
        self.obj_date0=datetime.datetime.strptime(strategy_start_time,'%Y%m%d')
        self.obj_date1=datetime.datetime.strptime(strategy_end_time,'%Y%m%d')
        self.df=df

    def hindcast_buy_and_hold(self):
        from buy_and_hold import buy_and_hold as strategy
               
        self.reffundflow=strategy(self.obj_date0, self.obj_date1, self.init_fund, self.df, 1.0)
    
    def hindcast_up_in_down_out(self):
        from up_in_down_out import up_in_down_out as strategy
        
        self.strategy_name='Up In & Down Out'
        self.fundflow=strategy(self.obj_date0, self.obj_date1, self.init_fund, self.df, 1.0)
        self.hindcast_buy_and_hold()

    
    def plot_funding_curve(self):
        ax = plt.subplot(111)
        plt.plot(self.reffundflow['value']+self.reffundflow['cash'], '-', color='gray', alpha=0.8, label='Buy & Hold')
        plt.title('Funding curve')
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
        plt.show()

