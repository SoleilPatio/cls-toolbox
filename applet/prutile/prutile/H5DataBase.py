# coding: utf-8
'''
Created on 2016年9月12日

@author: clouds
'''
import tables
import prutile.Utils as Utils
from prutile.Utils import DayCode
from prutile.DataStructure import AccessLog
from prutile.DataStructure import StockInfo
from prutile.DataStructure import DailyQuotation


class H5DataBase():
    def __init__(self):
        self.encoding = "ms950" 
        self.dirname = "d:\\"
        self.filename = "rutile_database.h5"
        self.h5file = tables.open_file(self.dirname + self.filename , mode = "a", title = "Rutile Database")
        
        #Create table "StockInfo" if not exist
        try:
            self.tbl_stockinfo = self.h5file.get_node('/', 'StockInfo')
        except:
            self.tbl_stockinfo = self.h5file.create_table("/", 'StockInfo', StockInfo, "stock info") #table need data structure
        
        #Create group "DailyQuotation" if not exist
        try:
            self.grp_dailyquotation = self.h5file.get_node('/', 'DailyQuotation')
        except:
            self.grp_dailyquotation = self.h5file.create_group('/', 'DailyQuotation', "Daily Quotation for each stocks")
            
        
        #point to daily quotation table of each stock, create when 1st access
        self.tbl_dailyquotation = {}
        
        
        #Create group "metadata" if not exist
        try:
            self.grp_metadata = self.h5file.get_node('/', 'metadata')
        except:
            self.grp_metadata = self.h5file.create_group('/', 'metadata', "Metadata of this file")
            
        
        #point to access log table, create when 1st access
        self.tbl_accesslog = {}
        
        #Attribute Test
        try:
            print("self.tbl_stockinfo.attrs.update_date " +self.tbl_stockinfo.attrs.update_date)
        except:
            pass
    
    
    
    def get_access_log_table(self, name ):
        table_name = "AccessLog" + "_" + name
        
        if table_name not in self.tbl_accesslog:
            try:
                self.tbl_accesslog[table_name] = self.h5file.get_node(self.grp_metadata, table_name)
            except:
                self.tbl_accesslog[table_name] = self.h5file.create_table(self.grp_metadata, table_name, AccessLog, "Access Log - " + table_name) 
                print("Create new table - %s / %s" % (self.grp_metadata._v_name, table_name) )
        
        return self.tbl_accesslog[table_name]
    
    
        
    def get_daily_quotation_table(self, market, code):
        table_name = market + "_" + code
        
        if table_name not in self.tbl_dailyquotation:
            try:
                self.tbl_dailyquotation[table_name] = self.h5file.get_node(self.grp_dailyquotation, table_name)
            except:
                self.tbl_dailyquotation[table_name] = self.h5file.create_table(self.grp_dailyquotation, table_name, DailyQuotation, "Daily Quotation -" + table_name) 
                print("Create new table - %s / %s" % (self.grp_dailyquotation._v_name, table_name) )
        
        return self.tbl_dailyquotation[table_name]
        
        
    def access_log_set(self, name, daycode, status, param1="", param2=""):
        if (name == None or name == ""):
            return
        
        table = self.get_access_log_table(name)
        
        in_daycode = daycode.to_int()
        update_count = 0
        for row in table.where("daycode == in_daycode" ):
            row['daycode'] = in_daycode
            row['status'] = status.encode(self.encoding, errors="replace")
            row['param1'] = param1.encode(self.encoding, errors="replace")
            row['param2'] = param2.encode(self.encoding, errors="replace")
            row.update()
            update_count += 1
            
        if( update_count == 0 ):
            #Add new
            row = table.row
            row['daycode'] = in_daycode
            row['status'] = status.encode(self.encoding, errors="replace")
            row['param1'] = param1.encode(self.encoding, errors="replace")
            row['param2'] = param2.encode(self.encoding, errors="replace")
            row.append()
        
        table.flush()
        
        
        
    def access_log_get_status(self, name, daycode):
        if (name == None or name == ""):
            return
        
        status = ""
        table = self.get_access_log_table(name)
        
        in_daycode = daycode.to_int()
        for row in table.where("daycode == in_daycode" ):
            status = row['status'].decode(self.encoding)
            
        return status
    
    
    def _stockinfo_set_row(self, row, stockinfo ):
        if hasattr(stockinfo, 'market'): row['market'] = stockinfo.market.encode(self.encoding, errors="replace")
        if hasattr(stockinfo, 'code'): row['code'] = stockinfo.code.encode(self.encoding, errors="replace")  #證券代號
        if hasattr(stockinfo, 'name'): row['name'] = stockinfo.name.encode(self.encoding, errors="replace")  #證券名稱
        if hasattr(stockinfo, 'category'): row['category'] = stockinfo.category.encode(self.encoding, errors="replace")  #(mops 股票分類(唯一))
        if hasattr(stockinfo, 'tags'): row['tags'] = stockinfo.tags.encode(self.encoding, errors="replace")  #(TWSE/YPEX 股票分類)
        if hasattr(stockinfo, 'company_name'): row['company_name'] = stockinfo.company_name.encode(self.encoding, errors="replace")  #公司名稱
        if hasattr(stockinfo, 'address'): row['address'] = stockinfo.address.encode(self.encoding, errors="replace")  #住址
        if hasattr(stockinfo, 'chairman'): row['chairman'] = stockinfo.chairman.encode(self.encoding, errors="replace")  #董事長
        if hasattr(stockinfo, 'general_manager'): row['general_manager'] = stockinfo.general_manager.encode(self.encoding, errors="replace")  #總經理
        if hasattr(stockinfo, 'establishment_daycode'): row['establishment_daycode'] = stockinfo.establishment_daycode  #成立日期
        if hasattr(stockinfo, 'list_daycode'): row['list_daycode'] = stockinfo.list_daycode  #上市日期 / 上櫃日期 / 興櫃日期 / 公開發行日期
        if hasattr(stockinfo, 'delist_daycode'): row['delist_daycode'] = stockinfo.delist_daycode  #下市日期
        if hasattr(stockinfo, 'par_value'): row['par_value'] = stockinfo.par_value.encode(self.encoding, errors="replace")  #普通股每股面額
        if hasattr(stockinfo, 'paid_in_capital'): row['paid_in_capital'] = stockinfo.paid_in_capital  #實收資本額(元)
        if hasattr(stockinfo, 'issued_share'): row['issued_share'] = stockinfo.issued_share  #已發行普通股數或TDR原發行股數
        if hasattr(stockinfo, 'private_placement_share'): row['private_placement_share'] = stockinfo.private_placement_share  #私募普通股(股)
        if hasattr(stockinfo, 'preferred_share'): row['preferred_share'] = stockinfo.preferred_share  #特別股(股)
    
    
    def stockinfo_set(self, stockinfo):
        
        update_count = 0
        key = stockinfo.code
        for row in self.tbl_stockinfo.where("code == key" ):
            self._stockinfo_set_row(row, stockinfo)
            row.update()
            update_count += 1
            
        if( update_count == 0 ):
            row = self.tbl_stockinfo.row
            #Add new record
            print("Add new StockInfo :" + stockinfo.code + " " + stockinfo.code)
            self._stockinfo_set_row(row, stockinfo)
            row.append()
            print("------------------------")    
        
        #flush
        self.tbl_stockinfo.flush()    
        
                
            
    def stockinfo_get_by_code(self, stock_code):

        table = self.tbl_stockinfo
        
        enc_stock_code = stock_code.encode(self.encoding, errors="replace")
        for row in table.where("code == enc_stock_code" ):
            ret_stockinfo = StockInfo()
            ret_stockinfo.market = row['market'].decode(self.encoding)
            ret_stockinfo.code = row['code'].decode(self.encoding)
            ret_stockinfo.name = row['name'].decode(self.encoding)
            ret_stockinfo.tags = row['tags'].decode(self.encoding)
            return ret_stockinfo
            
        return None
    
            
        
        
    def update_stock_info(self, stock_info ):
  
        for key in sorted(stock_info):
            self.stockinfo_set(stock_info[key])
        
        print("update [StockInfo] table %d entries." % len(stock_info))      
        #update attribute
        self.tbl_stockinfo.attrs.update_date = DayCode().__str__()
        #flush
        self.tbl_stockinfo.flush()  #flush the table I/O buffer if we want to write all this data to disk.
    
        
        
    def _update_daily_quotation(self, row, stock ):
        
            try:
                row['daycode'] = stock['daycode']
                row['change'] = stock['change']
                
                row['volume'] = Utils.to_int(stock['成交股數'])
                row['deal'] = Utils.to_int(stock['成交筆數'])
                row['amount'] = Utils.to_int(stock['成交金額'])
                row['open_price'] = Utils.to_float(stock['開盤價'])
                row['top_price'] = Utils.to_float(stock['最高價'])
                row['low_price'] = Utils.to_float(stock['最低價'])
                row['close_price'] = Utils.to_float(stock['收盤價'])
                
                row['final_reveal_buy_price'] = Utils.to_float(stock['最後揭示買價'])
                row['final_reveal_buy_vol'] = Utils.to_int(stock['最後揭示買量'])
                row['final_reveal_sell_price'] = Utils.to_float(stock['最後揭示賣價'])
                row['final_reveal_sell_vol'] = Utils.to_int(stock['最後揭示賣量'])
            except:
                raise ValueError('Parsing Error!')
        
            
            #Update StockInfo if this is not found in StockInfo
            if ( self.stockinfo_get_by_code( stock["證券代號"]) == None ):
                new_stockinfo = StockInfo()
                new_stockinfo.market = stock['market']
                new_stockinfo.code = stock['證券代號']
                new_stockinfo.name = stock['證券名稱']
                new_stockinfo.tags = ("UNKNOWN",)
                self.stockinfo_set(new_stockinfo)
                
            
            
            
            
        
    def update_daily_quotation(self, stock_dq):
        
        db_update_count = 0
        db_new_count = 0
        
        for stock in stock_dq:
            market = stock["market"]
            code = stock["證券代號"]
            dc_int = stock['daycode']
            table = self.get_daily_quotation_table(market, code)
            
            update_count = 0
            
            for row in table.where("daycode == dc_int" ):
                #Update old
#                 print("Update Daily Quotation(%d):%s" % (stock['daycode'], code))
                self._update_daily_quotation(row, stock )
                row.update()
                update_count += 1
            
            db_update_count += update_count
            if( update_count == 0 ):
                #Add new
#                 print("Add New Daily Quotation(%d):%s" % (stock['daycode'], code))
                row = table.row
                self._update_daily_quotation(row, stock)
                row.append()
                
                db_new_count += 1
            
            table.flush()
            
            
        print("Update [DailyQuotation] table %d entries. (update:%d / new:%d)" % ( len(stock_dq), db_update_count, db_new_count )  )          
        
        
        
                
        
    def close(self):
        self.h5file.close()
         
