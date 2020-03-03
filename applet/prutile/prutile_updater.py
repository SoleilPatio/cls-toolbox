# coding: utf-8
'''

@author: clouds
'''
from prutile.Utils import DayCode
from prutile.H5DataBase import H5DataBase
from prutile.WebContentMiner import Web_TwseDailyQuotation
from prutile.WebContentMiner import Web_TpexDailyQuotation
from prutile.Web_MopsBasicInfo import Web_MopsBasicInfo
    

           
           
def PR_UpdateLatestStockInfo(H5Db, DEBUG=False):
    
    #更新上市公司資訊
    today = DayCode() 
    DailyQ = Web_TwseDailyQuotation(H5Db)
    while True:
        #Part1: Stock Info (TWSE)
        stock_info = DailyQ.get_stock_info(today, DEBUG)
        if( len(stock_info) > 0 ):
            break
        else:
            today.go_prev_day()
      
    H5Db.update_stock_info(stock_info)
    
    
    #更新上櫃公司資訊
    today.today()
    DailyQ = Web_TpexDailyQuotation(H5Db)
    while True:
        #Part1: Stock Info (TWSE)
        stock_info = DailyQ.get_stock_info(today, DEBUG)
        if( len(stock_info) > 0 ):
            break
        else:
            today.go_prev_day()
    
    H5Db.update_stock_info(stock_info)
    

def PR_UpdateDailyQuotation(H5Db, start_datecode, end_datecode = DayCode().today(), DEBUG=False):
    DailyQ_twse = Web_TwseDailyQuotation(H5Db)
    DailyQ_tpex = Web_TpexDailyQuotation(H5Db)
    
    daycode = DayCode().copy_from( start_datecode )
    
    while daycode.to_int() <= end_datecode.to_int():
        #info
        percentage = 100*(daycode.to_int() - start_datecode.to_int()) / (end_datecode.to_int() - start_datecode.to_int())
        print("\n\n\n===>Progress: %s/[%s-%s] (%d%%).....\n" % (daycode, start_datecode, end_datecode, percentage ) )
    
        #上市行情
        stock_dq = DailyQ_twse.get_data(daycode, DEBUG)
        H5Db.update_daily_quotation(stock_dq)
        
        #上櫃行情
        stock_dq = DailyQ_tpex.get_data(daycode, DEBUG)
        H5Db.update_daily_quotation(stock_dq)
        
        #Advance one day
        daycode.go_next_day()
        
    
OPTION = {
    "update_stock_info" : True,
    "update_daily_quotation" : False
    }    

if __name__ == '__main__':
    DEBUG = True
    DEBUG = False
    
    '''
    #Open/Create database
    '''
    H5Db = H5DataBase()
    
    '''
    #Update Stockinfo : 更新公司資訊
    '''
    if( OPTION["update_stock_info"] ):
        PR_UpdateLatestStockInfo(H5Db, DEBUG)
    
    '''
    #Update Daily Quotation : 更新每日報價
    '''
    if( OPTION["update_daily_quotation"] ):
        if (DEBUG == True):
            start_date = DayCode().go_prev_day().go_prev_day()
        else:
            start_date = DayCode(93, 2, 11)
            
        PR_UpdateDailyQuotation(H5Db, start_date, DayCode().today(), DEBUG )
    
    
    
    '''
    #Test Zone
    '''

    StockInfo_mos = Web_MopsBasicInfo(H5Db)
     
    stock_info = StockInfo_mos.get_stock_info(DEBUG)
     
    H5Db.update_stock_info(stock_info)
     
    
    '''
    #Close file
    '''
    H5Db.close()
    
    

    print("\n\n\nDone!")
    
    
    