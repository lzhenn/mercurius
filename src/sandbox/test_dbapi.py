#!/usr/bin/env python


import pandas as pd
import sys

sys.path.append('../utils')
from aes_crypto import AESCipher
def mainfunc():
    pd_cre=pd.read_csv('../../credential/credential.csv', index_col='item')
    code =pd_cre.loc['mysql','cred']
    print(code)
    
    crypto_obj=AESCipher('Always Love You')
    print(crypto_obj.decrypt(code))

if __name__=='__main__':
    mainfunc()
