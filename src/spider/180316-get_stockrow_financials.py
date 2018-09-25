#/usr/bin/env python

"module for download US equity data daily from IEX api"

import datetime
import urllib.request
import os, time, random
# equity path
eq_path='/home/lzhenn/array/lzhenn/findata/equity'
eq_basics_path=eq_path+'/financials'

# equity list
eq_market=['NASDAQ','AMEX','NYSE']

statement=['Metrics','Growth','Cash%20Flow','Balance%20Sheet','Income%20Statement']


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
                for xls_itm in statement:
                    if not(os.path.isfile(eq_basics_path+'/'+symb[0]+'_'+xls_itm+'.xlsx')):
                        print('\n\nNow download %s %s@%s (%d)' % (symb[0], xls_itm,item, pos))
                        url='https://stockrow.com/api/companies/'+symb[0]+'/financials.xlsx?dimension=MRQ&section='+xls_itm
                        try:
                            req = urllib.request.Request(url, None, headers)
                            response = urllib.request.urlopen(req).read()
                            with open(eq_basics_path+'/'+symb[0]+'_'+xls_itm+'.xlsx', 'wb') as f:
                                f.write(response)
                        except Exception as E:
                            print('\n'+str(E))
                            print('\n\nDownload %s@%s (%d) Failed...' % (symb[0], item, pos))
                            if str(E) =='HTTP Error 404: Not Found':
                                break
                        sptime=random.randint(200,300)/10
                        print('\nsleep %4.2fs' % sptime)
                        time.sleep(sptime)
   
if __name__ == '__main__':
    mainfunc()
