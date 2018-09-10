
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

    def hindcast_up_in_down_out(self):
        from up_in_down_out import up_in_down_out as strategy
               
        self.fundflow=strategy(self.obj_date0, self.obj_date1, self.init_fund, self.df, 1.0)



    def plot_funding_curve(self):
        plt.plot(self.fundflow['value']+self.fundflow['cash'])
        buy_point=(self.fundflow['value']+self.fundflow['cash'])*self.fundflow['trade']
        buy_point=buy_point[buy_point>0]
        plt.plot(buy_point, 'o', mfc='red')

        sell_point=(self.fundflow['value']+self.fundflow['cash'])*(-1)*self.fundflow['trade']
        sell_point=sell_point[sell_point>0]
        plt.plot(sell_point, 'o', mfc='blue')
     
        plt.title('Funding curve')
        plt.show()
        

