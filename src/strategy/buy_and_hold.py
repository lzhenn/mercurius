#/usr/bin/env python

"Buy and hold strategy, the simplist strategy"

import datetime
import pandas as pd
import numpy as np

'''------------------------

df0       dataframe for the target
tg_name   target name (col name) in df0


'''
def buy_and_hold(initime_obj, outtime_obj, ini_fund, df0, tg_name, s_ratio):
    
    df_per_share=df0/s_ratio
    ini_price_per_share=df_per_share.loc[initime_obj]
    
    # All in
    max_share = int(ini_fund/ini_price_per_share)

    ini_eq=max_share*ini_price_per_share
    ini_cash=ini_fund-ini_eq
    
    ratio=ini_eq/df_per_share.loc[initime_obj]
    pd=ratio*df_per_share.loc[initime_obj:outtime_obj]
    return pd
