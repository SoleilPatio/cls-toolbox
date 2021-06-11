#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )

import os
import string

import libPython.core.util as util
import openpyxl


class ExcelfileOpenpyxl(object):
    def __init__(self):
        self.filename = None
        self.workbook = None

    """
    -----------------------------------------------
    Open/Save
    -----------------------------------------------
    """
    
    def Open(self, filename, data_only=False, read_only=False):
        if os.path.isfile(filename):
            self.workbook = openpyxl.load_workbook( filename = filename, data_only=data_only, read_only=read_only)
        else:
            self.workbook = openpyxl.Workbook()
            #remove 1st sheet that auto created by "not write_oly open"
            # self.workbook.remove(self.workbook[self.workbook.sheetnames[0]])
        self.filename = filename
    
    def Save(self):
        return self.SaveAs(self.filename)

    def SaveAs(self, out_filename):
        ret = self.workbook.save( filename = out_filename)
        msg = 'save file \"%s\"' % out_filename
        util.LogInfo(msg)
        return ret
        
    """
    -----------------------------------------------
    Properties
    -----------------------------------------------
    """
    def SheetList(self):
        return self.workbook.get_sheet_names()
             
    def GetSheetByName(self, sheet_name):
        return self.workbook[sheet_name]
     
    def GetSheetByIndex(self, index):
        return self.workbook[self.book.get_sheet_names()[index]]

    #...................................
    # max_row = current max valid row #
    # NOTE: max_row is 1 instead of 0 in new created empty sheet
    #...................................
    def max_row(self, sheet_obj=None):
        if sheet_obj:
            return sheet_obj.max_row
        else:
            return self.workbook.active.max_row

    def max_column(self, sheet_obj=None):
        if sheet_obj:
            return sheet_obj.max_row
        else:
            return self.workbook.active.max_column

    #...................................
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
        try:
            index = self.SheetList().index(sheet_name)
            self.workbook.active = index
        except:
            # Create a new sheet
            self.workbook.create_sheet(title=sheet_name)
            index = self.SheetList().index(sheet_name)
            self.workbook.active = index


    """
    -----------------------------------------------
    Write by ROWS
    -----------------------------------------------
    """
    def AppendRows(self, rows ):
        for row in rows:
            self.workbook.active.append(row)

        
        
"""
-----------------------------------------------
Unitest Functions
-----------------------------------------------
"""        
def TEST_case1_colname():
    excel = ExcelfileOpenpyxl()
    print(f'{excel.col_num("IVC")}')

def TEST_case2_change_active_sheet():
    excel = ExcelfileOpenpyxl()
    # excel.Open("test.xlsx",read_only=True)
    excel.Open("test.xlsx")
    excel.SetActiveSheet("Sheet1")
    print(f"max_row Sheet1={excel.max_row()}")
    excel.AppendRows([["sheet1", "sheet1", "sheet1",]])
    print(f"max_row Sheet1={excel.max_row()}")

    excel.SetActiveSheet("SheetYYYY")
    print(f"max_row SheetY={excel.max_row()}")
    excel.AppendRows([["SheetYYYY", "SheetYYYY", "SheetYYYY",]])
    print(f"max_row SheetY={excel.max_row()}")

    excel.SetActiveSheet("Sheet1")
    print(f"max_row Sheet1={excel.max_row()}")
    excel.AppendRows([["sheet11", "sheet11", "sheet11",]])
    print(f"max_row Sheet1={excel.max_row()}")

    excel.SetActiveSheet("SheetYYYY")
    print(f"max_row SheetY={excel.max_row()}")
    excel.AppendRows([["SheetYYYY2", "SheetYYYY2", "SheetYYYY2",]])
    print(f"max_row SheetY={excel.max_row()}")
    excel.Save()






if __name__ == '__main__':
    TEST_case1_colname()
    TEST_case2_change_active_sheet()

    # excel = ExcelfileOpenpyxl()
    # # excel.Open("test.xlsx",read_only=True)
    # excel.Open("test.xlsx")

    # row_meta = [[123]]
    # excel.WriteRows("meta",row_meta)
    # row_pri = [[321, "=A1+'meta'!$A$1"]]
    # excel.WriteRows("pri",row_pri)
    # excel.Save()
    
    
    print("Done!")
    
    
    
    pass
