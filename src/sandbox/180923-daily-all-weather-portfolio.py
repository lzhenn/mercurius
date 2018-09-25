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
    
    date_lastday=datetime.datetime.now()+datetime.timedelta(days=-1)
    date_startday=datetime.datetime.now()+datetime.timedelta(days=-366*2)
    date_strategy_startday=datetime.datetime.now()+datetime.timedelta(days=-365*1)
    date_str_last=date_lastday.strftime('%Y%m%d')
    date_str_start=date_strategy_startday.strftime('%Y%m%d')
    data_str_start_date=date_startday.strftime('%Y%m%d')
    adj_cycle=365
    ini_fund=10000.0

    with open (const.CFG_PORTFOLIO_FILE,'r') as f:
        tgt_json=json.load(f)
        portfolio=portfolio_pkg(tgt_json['portfolio_test'], data_str_start_date, date_str_start, date_str_last,adj_cycle,ini_fund)
        portfolio.drive_timing_strategy()


if __name__ == '__main__':
    mainfunc()
