#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )

"""
##################################################################
xlwings:
    pros:
        1. can read result of formula
    cons:
##################################################################
"""

import string
import libPython.core.util as util
import xlwings as xw



class ExcelfileXlwings(object):
    def __init__(self):
        self.filename = None
        self.workbook = None
        self.active_sheet = None #active shee object
    

    """
    -----------------------------------------------
    Open/Save
    -----------------------------------------------
    """
    
    def Open(self, filename):
        self.workbook = xw.Book(filename)
        self.filename = filename

    def Close(self):
        self.workbook.close()

    def Save(self):
        pass

    def SaveAs(self, out_filename):
        pass

    """
    -----------------------------------------------
    Properties
    -----------------------------------------------
    """
    def SheetList(self):
        ret = []
        for sheet in self.workbook.sheets:
            ret.append(sheet.name)
        return ret

    def GetSheetByName(self, sheet_name):
        for sheet in self.workbook.sheets:
            if sheet_name == sheet.name:
                return sheet
        return None

    def GetSheetByIndex(self, index):
        return self.workbook.sheets[index]

    def max_row(self, sheet_obj=None): #TODO
        if sheet_obj:
            return sheet_obj.cells(65536,1).end("up").row
        else:
            return self.active_sheet.cells(65536,1).end("up").row

    def max_column(self, sheet_obj=None):
        pass

    #...................................
    # common functions for all excel libraries
    # excel column name handling.
    # excel is 1-index (instead of 0-index)
    #...................................
    def col_name(self, col_num):
        retstr=""
        while col_num:
            remainder = (col_num-1) % 26
            retstr = chr(ord("A") + remainder ) + retstr
            col_num = int((col_num-remainder) / 26)
        return retstr

    def col_num(self, col_name):
        num = 0
        for c in col_name:
            if c in string.ascii_letters:
                num = num * 26 + (ord(c.upper()) - ord('A')) + 1
        return num

    """
    -----------------------------------------------
    Operation
    -----------------------------------------------
    """
    def SetActiveSheet(self, sheet_name):
        self.active_sheet = self.GetSheetByName(sheet_name)

    def active(self):
        return self.active_sheet

    #...................................
    # range_str = "A1:B10"
    #...................................
    def ReadRange(self, range ):
        # data = self.workbook.active[range]
        # data = [ [cell.value for cell in row] for row in data]
        # return data
        pass





    """
    ========================================================
    Misc (Not Interface)
    ========================================================
    """
    def ListOpenExcelFiles(self):
        ret = []
        for i, app in enumerate(xw.apps):
            print( "app",i,":")
            for book in app.books:
                print( "\t",book.name)
                ret.append(book.name)
        return ret
                
    
    def ParseSheetAsTable(self, sheet_obj):
        ret_table = []
        
        field_names = sheet_obj.range("A1").expand("right").value
        
        max_row = self.max_row(sheet_obj)
        max_col = len(field_names)
        print( "max_row=", max_row)
        print( "max_col=", max_col)
        
        
        records = sheet_obj.range(xw.Range("A2"),(max_row,max_col)).value
        print( field_names)
        
        for i, record in enumerate(records):
            r_dict = {}
            for j, value in enumerate(record):
                r_dict[field_names[j]] = value
            ret_table.append(r_dict)
            
        return ret_table
            
        
        
        
        


if __name__ == '__main__':
    filename = r"C:\\Users\\cloud\\OneDrive\\BIN\\cls-toolbox\\test.xlsx"
    
    xwobj = ExcelfileXlwings()
    
    xwobj.Open(filename)
    xwobj.ListOpenExcelFiles()
    xwobj.SheetList()
    
    sheet = xwobj.GetSheetByIndex(0)
    
    print( sheet.name)
    
    print ("last row of ", sheet.name, " is ",  xwobj.max_row(sheet))
    
    table = xwobj.ParseSheetAsTable(sheet)
    
    for r in table:
        print( r)
    
    
    
    
    pass