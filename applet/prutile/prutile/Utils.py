# coding: utf-8
'''
Created on 2016年9月12日

@author: clouds
'''
import time
import calendar

class DayCode:
    def __init__(self, year=int(time.strftime("%Y")), month=int(time.strftime("%m")), day=int(time.strftime("%d")) ):
        self.year = year + 1911 if year < 1911 else year
        self.month = month
        self.day = day
        
        
    def __str__(self):
        return "%d%02d%02d" % (self.year,self.month,self.day)

    def copy_from(self, daycode ):
        self.year = daycode.year
        self.month = daycode.month
        self.day = daycode.day
        return self
    
    
    def today(self):
        self.year=int(time.strftime("%Y"))
        self.month=int(time.strftime("%m"))
        self.day=int(time.strftime("%d"))
        
        return self
    
    def set_by_yy_mm_dd(self, yy, mm, dd):
        self.year = yy + 1911 if yy < 1911 else yy
        self.month = mm
        self.day = dd
        
        return self
        
    # ex. 90/07/23
    def set_by_yymmdd(self, date_string ):
        ds = date_string.split("/")
        self.set_by_yy_mm_dd(int(ds[0]), int(ds[1]), int(ds[2]))
        
        return self
        
        
        
    def tw_yy_mm_dd(self):
        return "%d/%02d/%02d" % ( self.year - 1911, self.month, self.day )
    
    def to_int(self):
        return int("%d%02d%02d" % (self.year,self.month,self.day))
    
    
    def _last_day_of_month(self, year, month):
        #find the last day of month
        cal = calendar.Calendar()
        monthdays = cal.monthdays2calendar(year, month)
        lastweek = monthdays[-1]
        for idx in range(-1, -len(lastweek)-1, -1):
            if lastweek[idx][0] != 0:
                last_day =  lastweek[idx][0]
                break
        return last_day
    
    def go_next_day(self):
        if(self.day >= 28):
            #find the last day of month
            last_day = self._last_day_of_month(self.year, self.month)
                
            if last_day > self.day:
                self.day += 1
            else:
                self.day = 1
                self.month += 1
                if self.month > 12 :
                    self.month = 1
                    self.year += 1

            
        else:
            self.day += 1
        
        return self
            
    def go_prev_day(self):
        if(self.day > 1):
            self.day -= 1
        else:
            self.month -= 1
            if self.month < 1:
                self.month = 12
                self.year -= 1
                
            #find the last day of month
            self.day = self._last_day_of_month(self.year, self.month)
        
        return self
        
        



def to_int(string):
    try:
        ret = int(string.replace(",", ""))
        return ret
    except:
        return 0
        #return None #Don't know why can not be none type
    
def to_float(string):
    try:
        ret = float(string.replace(",", ""))
        return ret
    except:
        return None
    
