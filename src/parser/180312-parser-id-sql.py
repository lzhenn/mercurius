#/usr/bin/env python

"module for download US equity data daily from robinhood private api"

import pymysql.cursors

# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity/instrument'

def mainfunc():
    
    connetion = pymysql.connect()


if __name__ == '__main__':
    mainfunc()
