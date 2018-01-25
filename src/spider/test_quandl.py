import pandas as pd
import numpy as np
import quandl

pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
quandl.ApiConfig.api_key =pd_cre.loc['quandl','cred']
mydata = quandl.get_table("CURRFX/USDCNY", rows=1)
print(mydata)
