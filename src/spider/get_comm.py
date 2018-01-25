#/usr/bin/env python

"module for download commodities data"

import pandas as pd
import numpy as np
import quandl


# comm path
comm_path='/home/lzhenn/array/lzhenn/findata/commodities/'
# comm list
comm=['LBMA/GOLD', 'LBMA/SILVER', 'EIA/PET_RWTC_D']


def mainfunc():
    pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
    quandl.ApiConfig.api_key =pd_cre.loc['quandl','cred']
    
    for item in comm:
        print(item)
        data_hdl=quandl.get(item)
        with open(comm_path+get_outname(item), 'w') as f:
            data_hdl.to_csv(f)

def get_outname(itemname):
    item=itemname.split('/')
    return item[1]+'-'+item[0]


if __name__ == '__main__':
    mainfunc()
