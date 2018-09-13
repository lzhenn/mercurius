#/usr/bin/env python

"drive singel strategy, and plot funding curve and basic info"

import json, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from const import const
from dbapi import mc_dbapi
from strategy_pkg import strategy_pkg 
from utils import parse_trading_day

def mainfunc():
    date_lastday=datetime.datetime.now()+datetime.timedelta(days=-1)
    date_startday=datetime.datetime.now()+datetime.timedelta(days=-366*11)
    date_strategy_startday=datetime.datetime.now()+datetime.timedelta(days=-366*10)
    date_str_last=date_lastday.strftime('%Y%m%d')
    date_str_start=date_startday.strftime('%Y%m%d')
    
    with open (const.CFG_PORTFOLIO_FILE,'r') as f:
        tgt_json=json.load(f)

    web_dic={}
    ii=0
    for tgt in tgt_json['symbols']:
        ii=ii+1
        print(tgt)    
        bbid_dic=mc_dbapi.fetch_bbid(tgt)
        df=mc_dbapi.fetch_ohlc(bbid_dic['bbid'],date_str_start,date_str_last)
        date_strategy_startday=parse_trading_day(df.index,date_strategy_startday)
        date_lastday=parse_trading_day(df.index,date_lastday)
        obj_strategy=strategy_pkg(tgt,df[['middle']],date_strategy_startday.strftime('%Y%m%d'),date_lastday.strftime('%Y%m%d'))
        obj_strategy.hindcast_up_in_down_out()
        obj_strategy.strategy_info()
        
        web_dic['target'+str(ii)]=obj_strategy.info
        
        obj_strategy.plot_funding_curve()
        plt.savefig(const.MERC_ROOT+'/routine_output/'+tgt+'.png')
        plt.close()
    with open(const.MERC_ROOT+'/routine_output/routine_info.json','w') as f:
        json.dump(web_dic,f)

if __name__ == '__main__':
    mainfunc()
