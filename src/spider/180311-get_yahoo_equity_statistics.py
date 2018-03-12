#/usr/bin/env python

"module for download US equity data daily from IEX api"

import datetime
import urllib.request

# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/'
# equity list
def mainfunc():
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.360' }
    url='https://finance.yahoo.com/quote/GNC/key-statistics?p=GNC'
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req).read()
    date_lastday=datetime.datetime.now()+datetime.timedelta(days=-1)
    date_str=date_lastday.strftime('%Y%m%d')
    with open(eq_path+'/market_'+date_str+'.html', 'w') as f:
        f.write(response.decode('utf-8'))
if __name__ == '__main__':
    mainfunc()
