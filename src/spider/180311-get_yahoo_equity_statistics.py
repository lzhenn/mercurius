#/usr/bin/env python

"module for download US equity data daily from IEX api"

import datetime
import urllib.request
import os, time, random
# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity'
eq_basics_path=eq_path+'/basics'

# equity list
eq_market=['NASDAQ','ETF','AMEX','NYSE']



# equity list
def mainfunc():

    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.360' }
    
    for item in eq_market:
        files=os.listdir(eq_path+'/'+item)
        pos=0
        for item0 in files:
            pos=pos+1
            fsize = os.path.getsize(eq_path+'/'+item+'/'+item0)
            if fsize > 100:
                symb=item0.split('.')
                if not(os.path.isfile(eq_basics_path+'/'+symb[0]+'_basics.html')):
                    print('\n\nNow download %s@%s (%d)' % (symb[0], item, pos))
                    url='https://finance.yahoo.com/quote/'+symb[0]+'/key-statistics?p='+symb[0]
                    try:
                        req = urllib.request.Request(url, None, headers)
                        response = urllib.request.urlopen(req).read()
                        with open(eq_basics_path+'/'+symb[0]+'_basics.html', 'w') as f:
                            f.write(response.decode('utf-8'))
                    except:
                        print('\n\nDownload %s@%s (%d) Failed...' % (symb[0], item, pos))

                    sptime=random.randint(20,200)/10
                    print('\nsleep %4.2fs' % sptime)
                    time.sleep(sptime)
   
if __name__ == '__main__':
    mainfunc()
