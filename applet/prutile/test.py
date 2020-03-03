'''
Created on 2016年9月10日

@author: clouds
'''
import unittest
import tables

import urllib.parse
import urllib.request

import bs4
import code
import re

import calendar
from prutile.Utils import DayCode

class Test(unittest.TestCase):


    def XtestPytable(self):
        h5file = tables.open_file("D:\\rutile_database.h5", "a")
        
        print("FILE OBJ:")
        print(h5file)
        
        
        print("NODE:")
        for node in h5file:
            print(node)
        
        
        print("GROUP:")
        for group in h5file.walk_groups():
            print(group)

        print(h5file.root.StockInfo.colnames)
        for name in h5file.root.StockInfo.colnames:
            print(name)
            print(h5file.root.StockInfo.coldtypes[name])
            print(h5file.root.StockInfo.coldtypes[name].shape)

        pass

    def XtestTpexHtml(self):
        #Configure parameters
        self.url = "http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php"
        self.param = {'l':'zh-tw',
                      'd':'105/09/26',
                      'se': 'EW',
                      's':'0,asc,0' }
        
        #1. POST Method
        data = urllib.parse.urlencode(self.param).encode('ascii')

        req = urllib.request.Request("http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php", data)
        print(req)
#         print("[url requested] : " + req.full_url + "?" + str(req.data.decode()))
        
        #2. Open URL & get charset encoding
        html = urllib.request.urlopen(req)
        self.encoding = html.headers.get_content_charset()
        
        #3. BS4 parser
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        print(soup)
        
    def XtestTpexHtml2(self):
        #Configure parameters
        self.url = "http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php?"
        self.param = {'l':'zh-tw',
                      'd':'105/09/26',
                      'se': 'EW',
                      's':'0,asc,0' }
        
        #1. POST Method
        request = urllib.request.Request(self.url, urllib.parse.urlencode(self.param).encode())
        json = urllib.request.urlopen(request).read().decode()
        
        print(json)
        
    def testCalendar(self):
        d = DayCode(2016, 9, 27)
        
        while d.to_int() < 20181107 :
            print( d.go_next_day() )
        
        while d.to_int() > 20170215:
            print( d.go_prev_day() )
            
        print( d.today())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPytable']
    unittest.main()