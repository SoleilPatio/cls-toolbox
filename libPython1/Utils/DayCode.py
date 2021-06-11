#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

class DayCode(object):
    def __init__(self, year=int(time.strftime("%Y")), month=int(time.strftime("%m")), day=int(time.strftime("%d")), hour=int(time.strftime("%H")), minute=int(time.strftime("%M")) ):
        self.year = year + 1911 if year < 1911 else year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        
    
    def set_from_epoch_sec(self, secs):
        t = time.localtime(secs)
        self.year = t.tm_year
        self.month = t.tm_mon
        self.day = t.tm_mday
        self.hour = t.tm_hour
        self.minute = t.tm_min
        
        return self
    
    def set_from_str(self, date_str, str_format ):
        """
        str_format: https://docs.python.org/2/library/time.html
        """
        secs = self.from_str_to_sec(date_str, str_format)
        self.set_from_epoch_sec(secs)
        return self
    
    
    def from_str_to_sec(self, date_str, str_format ):
        """
        str_format: https://docs.python.org/2/library/time.html
        """
        secs = time.mktime(time.strptime(date_str,str_format))
        return secs
    
    def from_sec_to_daytime_day(self, sec):
        return datetime.datetime.fromtimestamp(sec).date()
        
        
    
    
    def __str__(self):
        return "%d%02d%02d" % (self.year,self.month,self.day)
        
    def tw_yy_mm_dd(self):
        return "%d/%02d/%02d" % ( self.year - 1911, self.month, self.day )
    
    def to_int(self):
        return int("%d%02d%02d" % (self.year,self.month,self.day))
    
    def to_yyyymmddHHMM(self):
        return "%d%02d%02d%02d%02d" % ( self.year, self.month, self.day, self.hour, self.minute )
        





if __name__ == '__main__':
    print(DayCode().to_yyyymmddHHMM())
    pass