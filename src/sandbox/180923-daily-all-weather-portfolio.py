#/usr/bin/env python

"drive portfolio strategy, and plot funding curve and basic info"

import json, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from const import const
from dbapi import mc_dbapi
from portfolio_pkg import portfolio_pkg 

def mainfunc():
    
    date_lastday=datetime.datetime.now()+datetime.timedelta(days=-2)
    date_str_last=date_lastday.strftime('%Y%m%d')

    with open (const.CFG_PORTFOLIO_FILE,'r') as f:
        tgt_json=json.load(f)
        
        adj_cycle=tgt_json['port_adj_cycle']
        ini_fund=tgt_json['port_ini_fund']
        
        portfolio=portfolio_pkg(tgt_json['portfolio_test'], tgt_json['port_data_start_date'], tgt_json['port_hindcast_start_date'], date_str_last,adj_cycle,ini_fund)
        portfolio.drive_timing_strategy()
        print(portfolio.info['QQQ']['fundflow'])

if __name__ == '__main__':
    mainfunc()
