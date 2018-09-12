
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
        self.strategy_info()


    def strategy_info(self):
        
        """
        Return the strategy basic info
        
        Returns:
            * self.info (dict):
                
                'tgt_name'      target name
                'name'          strategy name
                'update_date'   update date (the last trading day) of the target
                
                'ttr'           total return (%)
                'arr'           annualized rate of return
                'barr'          annualized rate of return for benchmark strategy
                'maxd'          maximum drawdown
                'maxd_days'     maximum drawdown days
                'maxd_rtdays'   maximum drawdown return days
                'volat'         volatility
                'sharpe'        sharpe ratio
                'alpha'         alpha
                'beta'          beta
                
                '1monr'         1 month return (%)
                '3monr'         3 month return (%)
                '6monr'         6 month return (%)
                '1yrr'          1 year return (%)
                '3yrr'          3 year return (%)
                '5yrr'          5 year return (%)

                '1monr_ref'     1 month return (%)
                '3monr_ref'     3 month return (%)
                '6monr_ref'     6 month return (%)
                '1yrr_ref'      1 year return (%)
                '3yrr_ref'      3 year return (%)
                '5yrr_ref'      5 year return (%)

                'action'        buy (X%) / sell (Y%) / hold (Z%)
                'bias365'       % departure relative to the yearly refrence line
                'bias72'        % departure relative to the 72-day refrence line
                'bias24'        % departure relative to the 24-day refrence line
                'bias12'        % departure relative to the 12-day refrence line
                'bias6'         % departure relative to the 6-day refrence line
        """
        
        from const import const
        from utils import parse_trading_day
        #---------- prepare --------------
        self.info={}
        norisk_ratio=const.NO_RISK_RETURN
        trading_days_per_year=const.TRAD_DAYS_PER_YEAR
        
        delta_time=self.fundflow.index[-1]-self.fundflow.index[0]
        
        # funding curve 
        np_fund=self.fundflow['value'].values+self.fundflow['cash'].values
        ref_fund=self.reffundflow['value'].values+self.reffundflow['cash'].values


        # basic info 
        self.info['tgt_name']=self.target_name
        self.info['name']=self.strategy_name
        self.info['update_date']=self.data_end_time.strftime('%Y-%m-%d')

        # total return (%)
        self.info['ttr']=(np_fund[-1])/(np_fund[0])-1

        # total return for benchmark strategy (%)
        self.info['bttr']=(ref_fund[-1])/(ref_fund[0])-1
        
        # annualized rate of return
        self.info['arr']=((self.info['ttr']+1)**(1.0/delta_time.days)-1)*trading_days_per_year

        # annualized rate of return for benchmark strategy
        self.info['barr']=((self.info['bttr']+1)**(1.0/delta_time.days)-1)*trading_days_per_year

        # maximum drawdown and volatility
        pos=1
        maxd=0
        for value in np_fund[1:]:
            if maxd<(1-value/np_fund[0:pos].max()):
                maxd=1-value/np_fund[0:pos].max()
                pos=pos+1
        self.info['maxd']=maxd

        # volatility
        np_vol=np.log(np_fund[1:])-np.log(np_fund[0:-1])
        self.info['volat']=np_vol.std()*np.sqrt(trading_days_per_year)

        # Sharpe Ratio
        self.info['sharpe']=(self.info['arr']-norisk_ratio)/self.info['volat']

        # beta
        cov_mtx=np.cov(np_fund, ref_fund)
        self.info['beta']=cov_mtx[1,1]/np.var(ref_fund)

        # alpha
        self.info['alpha']=(self.info['arr']-norisk_ratio)-self.info['beta']*(self.info['barr']-norisk_ratio)

        # action
        position=self.fundflow['value'].values[-1]/np_fund[-1]
        if self.fundflow['trade'][-1] == 0:
            if position > 0.98:
                self.info['action']='Full'
            elif position <0.01:
                self.info['action']='Empty'
            else:
                self.info['action']='Hold ({:.2%})'.format(position)
        elif self.fundflow['trade'][-1] == 1:
            self.info['action']='Buy! ({:.2%})'.format(1-position)
        else:
            self.info['action']='Sell! ({:.2%})'.format(position)
        
        # 1 year return (%)
        day365ago=parse_trading_day(self.fundflow.index,self.data_end_time+datetime.timedelta(days=-365))
        self.info['1yrr']=ref_fund[-1]/self.reffundflow['value'].loc[day365ago.date()]-1


        # departure 365day
        ma_ref=self.reffundflow.loc[day365ago.date():]['value'].mean()
        self.info['bias365']=(ref_fund[-1]-ma_ref)/ma_ref


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
        #plt.show()

