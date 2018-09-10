#/usr/bin/env python

"drive singel strategy, and plot funding curve and basic info"

import json

from const import const
from dbapi import mc_dbapi
from strategy_pkg import strategy_pkg 

def mainfunc():
    with open (const.CFG_TARGET_FILE,'r') as f:
        tgt_json=json.load(f)

    print(tgt_json['symbols']) 
    bbid_dic=mc_dbapi.fetch_bbid(tgt_json['symbols'][0])
    df=mc_dbapi.fetch_ohlc(bbid_dic['bbid'],tgt_json['start_date'],tgt_json['end_date'])
    obj_strategy=strategy_pkg(tgt_json['symbols'][0],df[['close']],tgt_json['strategy_start_date'],tgt_json['strategy_end_date'])
    obj_strategy.hindcast_up_in_down_out()
    obj_strategy.plot_funding_curve()
if __name__ == '__main__':
    mainfunc()
