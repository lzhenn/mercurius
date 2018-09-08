#/usr/bin/env python

"""Class Strategy

This class is the motherboard for any hindcastable strategy. 

"""

import datetime
import pandas as pd
import numpy as np

class strategy(object):
    """
    Args:
        * target_name (str): name of the targeted object
        * df (pandas dataframe): dataframe of the target historical values
            df sample:
            ID    TIMESTAMP     VALUE
            1     2018-08-29    112.5  
            2     2018-08-30    113.1
        * ini_fund (float): initial fund to invest in the target
    """
    def __init__(self,target_name, df, init_fund):
        self.target_name=target_name
        self.init_fund=init_fund
        self.start_time=df.loc
