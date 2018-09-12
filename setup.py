#!/usr/bin/env python

import os, json

def setup():
    path_dic={}
    
    path_dic['MERC_ROOT']                       =   os.path.abspath('.')
    path_dic['NO_RISK_RETURN']                  =   0.03
    path_dic['TRAD_DAYS_PER_YEAR']              =   252.0

    with open("./config_files/basic_info.json","w") as f:
        json.dump(path_dic,f)

if __name__=='__main__':
    setup()
