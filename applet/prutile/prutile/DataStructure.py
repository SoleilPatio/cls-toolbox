# coding: utf-8
'''
Created on 2016年9月12日

@author: clouds
'''

import tables


class AccessLog(tables.IsDescription):
    daycode = tables.UInt32Col()
    status = tables.StringCol(32)
    param1 = tables.StringCol(32)
    param2 = tables.StringCol(32)
    
#Access Log Status
class AL_STATUS:
    OK = "ok"
    BEYOND_RANGE = "beyond_range" #data is not valid in this day because it's too old
    EMPTY = "empty"
    ERROR = "error"
    DISCONNECT = "disconnect"




class StockInfo(tables.IsDescription):
    market = tables.StringCol(32)
    code = tables.StringCol(32)     #證券代號
    name = tables.StringCol(32)     #證券名稱
    category = tables.StringCol(32) #(mops 股票分類(唯一))
    tags = tables.StringCol(128)    #(TWSE/YPEX 股票分類)
    company_name = tables.StringCol(64) #公司名稱
    address = tables.StringCol(128) #住址
    chairman = tables.StringCol(32) #董事長
    general_manager = tables.StringCol(32) #總經理
    establishment_daycode = tables.UInt32Col() #成立日期
    list_daycode = tables.UInt32Col() #上市日期 / 上櫃日期 / 興櫃日期 / 公開發行日期
    delist_daycode = tables.UInt32Col() #下市日期
    par_value = tables.StringCol(32) #普通股每股面額
    paid_in_capital = tables.UInt64Col() #實收資本額(元)
    issued_share = tables.UInt64Col() #已發行普通股數或TDR原發行股數
    private_placement_share = tables.UInt64Col() #私募普通股(股)
    preferred_share = tables.UInt64Col() #特別股(股)
        

class DailyQuotation(tables.IsDescription):
    daycode = tables.UInt32Col()
    volume = tables.UInt64Col()         #成交股數
    deal = tables.UInt64Col()           #成交筆數
    amount = tables.UInt64Col()         #成交金額
    open_price =  tables.Float32Col()    #開盤價
    top_price =  tables.Float32Col()     #最高價
    low_price =  tables.Float32Col()     #最低價
    close_price = tables.Float32Col()    #收盤價
    change = tables.Float32Col()         #漲跌價差
    final_reveal_buy_price = tables.Float32Col()     #最後揭示買價
    final_reveal_buy_vol = tables.UInt64Col()       #最後揭示買量
    final_reveal_sell_price = tables.Float32Col()    #最後揭示賣價
    final_reveal_sell_vol = tables.UInt64Col()      #最後揭示賣量
    
    
    