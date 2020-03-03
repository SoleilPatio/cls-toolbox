# coding: utf-8
'''
Created on 2016年9月12日

@author: clouds
'''
import urllib.parse
import urllib.request
import bs4
import code
import re
import time
from enum import Enum 


import prutile.Utils as Utils 
from prutile.Utils import DayCode
from prutile.DataStructure import AL_STATUS
from prutile.DataStructure import StockInfo

#exception
import http.client

class WebContentMiner():
    def __init__(self, h5db ):
        self.url = ""
        self.param = {}
        self.encoding = ""
        self.h5db = h5db
        self.web_site_too_busy_string = "" #ex. "查詢過於頻繁"
        
        self.retry_interval_sec = 10    #retry interval when abnormal connection found
    

        
        
    def _get_bs_obj(self, daycode = DayCode()):
        soup = None
        
        #1. Generate URL (POST Method)
        data = urllib.parse.urlencode(self.param).encode('ascii')
        
        if (True): #embedded data into url directly (for tpex web site to work properly
            full_url = self.url + "?" + data.decode()
            req = urllib.request.Request(full_url)
            print("[url requested] : " + full_url )
        else:
            req = urllib.request.Request(self.url, data)
            print("[url requested] : " + req.full_url + "?" + str(req.data.decode()))
        
        
        
        #2. Try to connect
        CONN_STATUS = Enum("CONN_STATUS", "OK DISCONNECT ERROR BUSY NA")
        RETRY_COUNT = {
                       CONN_STATUS.OK : 0 ,
                       CONN_STATUS.DISCONNECT : 2,
                       CONN_STATUS.ERROR : 2,
                       CONN_STATUS.BUSY : 20,
                       CONN_STATUS.NA : 1
                       }
        
        status = CONN_STATUS.NA
        retry = RETRY_COUNT[status]
        
        while( retry > 0 ):
            
            if( status != CONN_STATUS.NA ):
                retry -= 1
                print("Retry in %d secs (%d/%d)" % (self.retry_interval_sec, retry+1, RETRY_COUNT[status] ))
                time.sleep(self.retry_interval_sec)
                
            try:
                html = urllib.request.urlopen(req)
                
            except http.client.RemoteDisconnected as err:
                print("連線錯誤:Remote disconnected! : ", err )
                if (status != CONN_STATUS.DISCONNECT ):
                    status = CONN_STATUS.DISCONNECT
                    retry = RETRY_COUNT[status]
                self.access_log_set(daycode, AL_STATUS.DISCONNECT)
                continue
                
            except urllib.error.URLError as err:
                print("連線錯誤:Connect error! : ", err )
                if (status != CONN_STATUS.ERROR ):
                    status = CONN_STATUS.ERROR
                    retry = RETRY_COUNT[status]
                self.access_log_set(daycode, AL_STATUS.ERROR)
                continue
            
            
            
            #2.1. get charset encoding
            self.encoding = html.headers.get_content_charset()
            
            #2.2. BS4 parser
            soup = bs4.BeautifulSoup(html, 'html.parser')
        
            #2.3. Check if web content is not valid due to too busy access
            if (self.web_site_too_busy_string != "" and 
                len( soup.find_all(string=re.compile(self.web_site_too_busy_string))) > 0 ):
                print("網頁忙碌 : " + self.web_site_too_busy_string )
                if (status != CONN_STATUS.BUSY ):
                    status = CONN_STATUS.BUSY
                    retry = RETRY_COUNT[status]
                continue
        
        
            #Finally....
            status = CONN_STATUS.OK
            retry = RETRY_COUNT[status]
        
        
        
        
        return soup
    
    
    def parse_table(self, fields_name_tr, data_tbody ):
        ret_stock_list = []
        
        #1. get field name index map
        ifn = [] #index to field name
        field_tag = fields_name_tr.find_all()[0].name #maybe "td" or "th"
        for field in fields_name_tr.find_all(field_tag):
            if( field.text.strip() not in ifn ): #avoid same field name
                ifn.append(field.text.strip())
        
            
        #2. main data
        for tr in data_tbody.find_all("tr"):  #for each row (stock)
            stock = {}
            fi = 0 #field index
            for td in tr.find_all("td"):     #for each data (field)
                if fi < len(ifn):
                    stock[ifn[fi]] = td.text.strip()
                    fi += 1
                else:
                    break
            if( len(stock) > 0 ):
                ret_stock_list.append(stock)
            
            
        #3. return
        return ret_stock_list


    def access_log_set(self, daycode, status, param1 = "", param2 = "" ):
        self.h5db.access_log_set(self.access_log_name, daycode, status, param1, param2 )
    
    def access_log_get_status(self, daycode):
        return self.h5db.access_log_get_status(self.access_log_name, daycode)
        
    def status_check_return_now(self, daycode):         
        #check 1: access log status check
        status = self.access_log_get_status(daycode)
        if (status == AL_STATUS.OK or status == AL_STATUS.BEYOND_RANGE):
            print( "Data Status: %s , pass!" % (status))
            return True
            
        
        #check 2: date before valid
        if daycode.to_int() < self.sincewhen.to_int():
            self.access_log_set(daycode, AL_STATUS.BEYOND_RANGE)
            return True
        
        return False
        
        
'''
上市公司每日行情
Since 93年2月11日 2004/2/11
'''    
class Web_TwseDailyQuotation(WebContentMiner):
    def __init__(self, h5db):
        #Inherit 
        super().__init__(h5db)
        
        #earliest date valid
        self.sincewhen = DayCode(93, 2, 11)
        
        #access log name
        self.access_log_name = "TwseDailyQuotation"
        
        #Configure URL parameters
        self.url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php"
        self.param = {'qdate':'105/06/02',
                      'selectType':'MS',
                      'download': '' }
        self.encoding = None
        
        
    def _config_url(self, daycode, selectType='MS'):
        #0. Prepare param
        self.param["qdate"] = daycode.tw_yy_mm_dd()
        self.param["selectType"] = selectType
    
    
    def get_stock_info(self, daycode, DEBUG=False ):
        #0. Return structure
        ret_stock_info = {}
        stock_list = []
        
        if daycode.to_int() < self.sincewhen.to_int():
            return ret_stock_info
        
        #1.Get soup object (1st time)
        self._config_url(daycode)
        soup = self._get_bs_obj(daycode)
        
        if(soup == None):
            return ret_stock_info
        
        #2. Get option to retrieve stock categories
        options = soup.select("#main-content   form   select option")
        '''
            "MS":大盤統計資訊
            "MS2":委託及成交統計資訊
            "ALL":全部
            "ALLBUT0999":全部(不含權證、牛熊證、可展延牛熊證)
            "0049":封閉式基金
            "0099P":ETF
            "019919T":受益證券
            "0999":認購權證(不含牛證)
            "0999P":認售權證(不含熊證)
            "0999C":牛證(不含可展延牛證)
            "0999B":熊證(不含可展延熊證)
            "0999X":可展延牛證
            "0999Y":可展延熊證
            "0999GA":附認股權特別股
            "0999GD":附認股權公司債
            "0999G9":認股權憑證
            "CB":可轉換公司債
            "01":水泥工業
            "02":食品工業
            "03":塑膠工業
            "04":紡織纖維
            "05":電機機械
            "06":電器電纜
            "07":化學生技醫療
            "21":化學工業
            "22":生技醫療業
            "08":玻璃陶瓷
            "09":造紙工業
            "10":鋼鐵工業
            "11":橡膠工業
            "12":汽車工業
            "13":電子工業
            "24":半導體業
            "25":電腦及週邊設備業
            "26":光電業
            "27":通信網路業
            "28":電子零組件業
            "29":電子通路業
            "30":資訊服務業
            "31":其他電子業
            "14":建材營造
            "15":航運業
            "16":觀光事業
            "17":金融保險
            "18":貿易百貨
            "9299":存託憑證
            "23":油電燃氣業
            "19":綜合
            "20":其他
        '''
        
        stock_cat = {} #==> { "01":"水泥工業" }
        for op in options:
            if op["value"] in ("ALL", "ALLBUT0999", "MS", "MS2",
                               "0049","0999","0999P","0999C","0999B",
                               "0999X","0999Y","0999GA","0999GD","0999G9","CB",): #exclude 2 ALLs categories
                continue
            stock_cat[op["value"]] = op.text.strip()
    
        
        #3. Get stock daily quotation (2nd time bs obj)
        for cat in sorted(stock_cat): #for each category
            print("List tags " + stock_cat[cat] + "...")
            self._config_url(daycode, cat)
            soup = self._get_bs_obj(daycode)
            try:
                fields_name_tr = soup.select("#main-content table thead tr")[1] #   tr:nth-child(2)
            except:
                print("table not valid.")
                continue
            
            data_tbody = soup.select("#main-content   table   tbody")[0]
            
            #3-1. Parse Table
            temp_sl = self.parse_table(fields_name_tr, data_tbody)
            for stock in temp_sl:
                stock["cat"] = stock_cat[cat]
            
            #3-2. append all to return list
            stock_list.extend(temp_sl)
            
            if(DEBUG==True):    
                break  #DEBUG: run only one category,only for debug             
            
        
        #4. Prepare to return
        for stock in stock_list:
            #fill a stock data
            code = stock["證券代號"]
            name = stock["證券名稱"]
            cat = stock["cat"]
            
            if code not in ret_stock_info:
                ret_stock_info[code] = StockInfo()
                ret_stock_info[code].tags = ""
            
#             ret_stock_info[code].market = "TWSE"
            ret_stock_info[code].code = code
            ret_stock_info[code].name = name
            ret_stock_info[code].tags = ret_stock_info[code].tags + "/" + cat

        
        #5. Info
        print("[info] Stock Info (%s): %d stocks done." % (daycode, len(ret_stock_info)))
        
        #6 return
        return  ret_stock_info
            
        
    
    
    def get_data(self, daycode, DEBUG=False ):
        
        stock_list = []
        
        #check status from access log to decide if return directly
        if (self.status_check_return_now(daycode) == True ):
            return stock_list
        
        
        #1.Get soup object
        if (DEBUG == False):
            self._config_url(daycode, 'ALLBUT0999')
        else:
            self._config_url(daycode, '01')
                 
        soup = self._get_bs_obj(daycode)
        
        if(soup == None):
            return stock_list
        
        #2.Try to find "每日收盤行情" table
        table = None
        for tb in soup.find_all("table"):
            if( len( tb.find_all(string=re.compile("每日收盤行情"))) == 1 ):
                table =tb #table found
                break
            
        if (table == None):
            self.access_log_set(daycode, AL_STATUS.EMPTY)
            print("table not valid.")
            return stock_list
        
        #3. Fields Name
        fields_name_tr = table.select("thead tr")[1]
        data_tbody = table.select("tbody")[0]
        
        #4. Parse Table
        stock_list = self.parse_table(fields_name_tr, data_tbody)
        
        
        #5. Append market
        for stock in stock_list:
            stock["daycode"] = daycode.to_int()
            stock["market"] = "TWSE"
            #mapping
            if stock['漲跌(+/-)'] == '－':
                stock['change'] = 0 - Utils.to_float(stock['漲跌價差'].replace(",", ""))
            else:
                stock['change'] = Utils.to_float(stock['漲跌價差'].replace(",", ""))
       
       
        #6. Info
        self.access_log_set(daycode, AL_STATUS.OK, param1=str(len(stock_list)) )
        print("上市行情 (%s): %d stocks done." % (daycode, len(stock_list)))
        
        #7. return
        return stock_list
    
    

'''
上櫃公司每日行情
Since 96年7月 2007/07/01
'''    
class Web_TpexDailyQuotation(WebContentMiner):
    def __init__(self,h5db):
        #Inherit 
        super().__init__(h5db)
        
        #earliest date valid
        self.sincewhen = DayCode(96, 7, 1)
        
        #access log name
        self.access_log_name = "TpexDailyQuotation"
        
    
        
    def _config_url_web_format(self):
        #Configure parameters
        self.url = "http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430.php"
        self.param = {'l':'zh-Tw'}
        self.encoding = None
        
        
    def _config_url_print_format(self, daycode, selectType ):
        #Configure parameters
        #Somehow tpex web site cannot be access right by python post method
        self.url = "http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_print.php"
        self.param = {'l':'zh-tw',
                      'd':'105/09/26',
                      'se': 'EW',
                      's':'0,asc,0' }
        self.encoding = None
        
        #0. Prepare param
        self.param["d"] = daycode.tw_yy_mm_dd()
        self.param["se"] = selectType
        
        
            
    
    def get_stock_info(self, daycode, DEBUG=False ):
        #0. Return structure
        ret_stock_info = {}
        stock_list = []
        
        if daycode.to_int() < self.sincewhen.to_int():
            return ret_stock_info
        
        #1.Get soup object (1st time)
        self._config_url_web_format()
        soup = self._get_bs_obj(daycode)
        
        if(soup == None):
            return ret_stock_info
        #2. Get option to retrieve stock categories
        #sect
        options = soup.select("#sect option")
        '''
            02 : 食品工業
            03 : 塑膠工業
            04 : 紡織纖維
            05 : 電機機械
            06 : 電器電纜
            21 : 化學工業
            08 : 玻璃陶瓷
            10 : 鋼鐵工業
            11 : 橡膠工業
            14 : 建材營造
            15 : 航運業
            16 : 觀光事業
            17 : 金融業
            18 : 貿易百貨
            20 : 其他
            22 : 生技醫療類
            23 : 油電燃氣類
            24 : 半導體類
            25 : 電腦及週邊類
            26 : 光電業類
            27 : 通信網路類
            28 : 電子零組件類
            29 : 電子通路類
            30 : 資訊服務類
            31 : 其他電子類
            32 : 文化創意業
            33 : 農業科技業
            80 : 管理股票
            AA : 受益證券
            EE : 上櫃指數股票型基金(ETF)
            TD : 台灣存託憑證(TDR)
            WW : 認購售權證
            GG : 認股權憑證
            BC : 牛證熊證
            EW :  所有證券(不含權證、牛熊證)
            AL :  所有證券 
            OR :  委託及成交資訊(16:05提供)
        '''
        
        stock_cat = {} #==> { "01":"水泥工業" }
        for op in options:
            if op["value"] in ("AA", "WW", "GG", "BC",
                               "EW","AL","OR",): #exclude categories 
                continue
            stock_cat[op["value"]] = op.text.strip()
    
        
        #3. Get stock daily quotation (2nd time bs obj)
        for cat in sorted(stock_cat): #for each category
            print("List tags " + stock_cat[cat] + "...")
            self._config_url_print_format(daycode, cat)
            soup = self._get_bs_obj(daycode)
            try:
                fields_name_tr = soup.select("body > table > thead > tr")[1] #body > table > thead > tr:nth-child(2)
            except:
                print("table not valid.")
                continue
            
            data_tbody = soup.select("body > table > tbody")[0]
            
            #3-1. Parse Table
            temp_sl = self.parse_table(fields_name_tr, data_tbody )
            for stock in temp_sl:
                stock["cat"] = stock_cat[cat]
            
            #3-2. append all to return list
            stock_list.extend(temp_sl)
            
            if(DEBUG==True):    
                break  #DEBUG: run only one category,only for debug             
            
        
        #4. Prepare to return
        for stock in stock_list:
            #fill a stock data
            code = stock["代號"]
            name = stock["名稱"]
            cat = stock["cat"]
            
            if code not in ret_stock_info:
                ret_stock_info[code] = StockInfo()
                ret_stock_info[code].tags = ""
            
#             ret_stock_info[code].market = "TPEX"
            ret_stock_info[code].code = code
            ret_stock_info[code].name = name
            ret_stock_info[code].tags = ret_stock_info[code].tags + "/" + cat

        
        #5. Info
        print("[info] Stock Info (%s): %d stocks done." % (daycode, len(ret_stock_info)))
        
        #6 return
        return  ret_stock_info
            
        
    
    
    def get_data(self, daycode, DEBUG=False ):
        stock_list = []
        
        #check status from access log to decide if return directly
        if (self.status_check_return_now(daycode) == True ):
            return stock_list
        
        #1.Get soup object
        if (DEBUG == False):
            if ( daycode.to_int() >= 20120529 ): #Use EW after 101/05/29
                self._config_url_print_format(daycode, 'EW')
            else:
                self._config_url_print_format(daycode, 'AL')
        else:
            self._config_url_print_format(daycode, '02')
        
        soup = self._get_bs_obj(daycode)
                 
        if(soup == None):
            return stock_list
        #2.Try to find "每日收盤行情" table
        table = None
        for tb in soup.find_all("table"):
            if( len( tb.find_all(string=re.compile("每日收盤行情"))) == 1 ):
                table =tb #table found
                break
            
        if (table == None):
            self.access_log_set(daycode, AL_STATUS.EMPTY)
            print("table not valid.")
            return stock_list
        
        #3. Fields Name
        fields_name_tr = table.select("thead tr")[1]
        data_tbody = table.select("tbody")[0]
        
        #4. Parse Table
        stock_list = self.parse_table(fields_name_tr, data_tbody)
        
        
        #5. Append market
        for stock in stock_list:
            stock["daycode"] = daycode.to_int()
            stock["market"] = "TPEX"
            stock["change"] = Utils.to_float( stock["漲跌"].replace(" ","") )
            #mapping
            stock['證券代號'] = stock['代號']
            stock['證券名稱'] = stock['名稱']
            stock['成交金額'] = stock['成交金額(元)']
            stock['開盤價'] = stock['開盤']
            stock['最高價'] = stock['最高']
            stock['最低價'] = stock['最低']
            stock['收盤價'] = stock['收盤']
            
            stock['最後揭示買價'] = stock['最後買價']
            stock['最後揭示買量'] = ""
            stock['最後揭示賣價'] = stock['最後賣價']
            stock['最後揭示賣量'] = ""
       
        #6. Info
        self.access_log_set(daycode, AL_STATUS.OK, str(len(stock_list)))
        print("上櫃行情 (%s): %d stocks done." % (daycode, len(stock_list)))
        
        #7. return
        return stock_list
    
    