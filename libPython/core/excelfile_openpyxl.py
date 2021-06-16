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
        self.chartobj_lookup = {}

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
        try:
            return self.workbook[sheet_name]
        except:
            return None
     
    def GetSheetByIndex(self, index):
        try:
            return self.workbook[self.book.get_sheet_names()[index]]
        except:
            return None

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
    ========================================================
    Chart Operation APIs
    ========================================================
    """
    """
    -----------------------------------------------
    Return openpyxl chart object of a designated sheet
    chart_type:
        "scatter"
    -----------------------------------------------
    """
    def GetChartObject(self, chart_type, sheet_name):
        self.chartobj_lookup[sheet_name] = self.chartobj_lookup.get(sheet_name, {})
        self.chartobj_lookup[sheet_name][chart_type] = self.chartobj_lookup[sheet_name].get(chart_type, {})
        chart_info = self.chartobj_lookup[sheet_name][chart_type]

        if chart_info:
            return chart_info["chart_obj"] #return chart object

        #Create a new chart object
        if chart_type == "scatter":
            chart_info["chart_obj"] = openpyxl.chart.ScatterChart()
            chart_info["id"] = len(self.chartobj_lookup[sheet_name]) - 1
            util.LogInfo(f"Create chart object:{chart_type}")
        elif chart_type == "bar":
            chart_info["chart_obj"] = openpyxl.chart.BarChart()
            chart_info["id"] = len(self.chartobj_lookup[sheet_name]) - 1
            util.LogInfo(f"Create chart object:{chart_type}")
        else:
            util.LogError(f"Unsupport chart type: {chart_type}")
            return None

        chart_obj = chart_info["chart_obj"]

        #initial position
        width = 10
        height = 18
        chart_pos = f"{self.col_name(chart_info['id'] * width + 1)}{ int(chart_info['id']/4)*height + 1 }"

        #Get sheet
        sheet_obj = self.GetSheetByName(sheet_name)
        if not sheet_obj:
            sheet_obj = self.workbook.create_sheet(title=sheet_name)

        #Add chart to sheet (can only do once)
        sheet_obj.add_chart(chart_obj, chart_pos)

        return chart_obj


    """
    -----------------------------------------------
    val_desc_obj = {"sheet":sheet_name, "min_row":2, "min_col":3, "max_col": 65535}
    name_cell = "'primary'!$A$1"
    -----------------------------------------------
    """
    """
    -----------------------------------------------
    Scatter Chart
        StrRefWorkaround:
            1.True : to workaround always set title_from_data=true but actually no
                1-1: in y_value_reference, "min_col" = "min_col"-1
                1-2: if title_from_data not set to True, can set title to reference string "=Sheet!$A$1"

    -----------------------------------------------
    """
    def AddScatterChart(self, x_val_desc_obj, y_val_desc_obj, name_cell, sheet_name="CHART_SHEET", StrRefWorkaround=True):
        chart_obj = self.GetChartObject("scatter", sheet_name)
        series = self.CreateSeries(x_val_desc_obj, y_val_desc_obj, name_cell, StrRefWorkaround=StrRefWorkaround)
        chart_obj.series.append(series)


    def CreateSeries(self, x_val_desc_obj, y_val_desc_obj, name_cell, StrRefWorkaround=True):
        ws = self.GetSheetByName(x_val_desc_obj["sheet"])
        x_val_desc_obj = dict(x_val_desc_obj)
        del x_val_desc_obj["sheet"]
        xvalues = openpyxl.chart.Reference(ws, **x_val_desc_obj)

        ws = self.GetSheetByName(y_val_desc_obj["sheet"])
        y_val_desc_obj = dict(y_val_desc_obj)
        del y_val_desc_obj["sheet"]
        #...................................
        # title_from_data=True workaround
        #...................................
        if StrRefWorkaround:
            y_val_desc_obj["min_col"] = y_val_desc_obj["min_col"]-1
        yvalues = openpyxl.chart.Reference(ws, **y_val_desc_obj)
        series = openpyxl.chart.Series(yvalues, xvalues, title_from_data=True) # NOTE: title_from_data must be set to True for latter StrRef setting
        series.tx.strRef = openpyxl.chart.data_source.StrRef( name_cell )

        return series

    """
    -----------------------------------------------
    val_desc_obj = {"sheet":sheet_name, "min_row":2, "min_col":3, "max_col": 65535}
    name_cell = "'primary'!$A$1"
    -----------------------------------------------
    """
    """
    -----------------------------------------------
    Bar Chart (category (x_value) can only be column )
        from_rows : 
            1. default is False, let data can only be vertical arranged
            2. set to True for my convenience
    -----------------------------------------------
    """
    def AddBarChart(self, x_val_desc_obj, y_val_desc_obj, name_cell, sheet_name="CHART_SHEET", from_rows=True):
        chart_obj = self.GetChartObject("bar", sheet_name)

        # Get Categories
        ws = self.GetSheetByName(x_val_desc_obj["sheet"])
        x_val_desc_obj = dict(x_val_desc_obj)
        del x_val_desc_obj["sheet"]
        xvalues = openpyxl.chart.Reference(ws, **x_val_desc_obj)

        # Get data
        ws = self.GetSheetByName(y_val_desc_obj["sheet"])
        y_val_desc_obj = dict(y_val_desc_obj)
        del y_val_desc_obj["sheet"]
        yvalues = openpyxl.chart.Reference(ws, **y_val_desc_obj)

        # Add to BarChart
        chart_obj.add_data(yvalues, titles_from_data=False, from_rows=from_rows)
        chart_obj.set_categories(xvalues)
        


        
"""
-----------------------------------------------
Unitest Functions
-----------------------------------------------
"""        
def TEST_1_colname():
    excel = ExcelfileOpenpyxl()
    print(f'{excel.col_num("IVC")}')

def TEST_2_change_active_sheet():
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

def TEST_3_chart():
    excel = ExcelfileOpenpyxl()
    excel.Open("test.xlsx")

    for i in range(10):
        x_val_desc_obj = {"sheet":"Sheet", "min_row":1, "min_col":3, "max_col": 7}
        y_val_desc_obj = {"sheet":"Sheet", "min_row":2, "min_col":3, "max_col": 7}
        name_cell = "'sheet'!$A$1"
        excel.AddScatterChart(x_val_desc_obj, y_val_desc_obj, name_cell)


        x_val_desc_obj = {"sheet":"Sheet", "min_row":1, "min_col":3, "max_col": 7}
        y_val_desc_obj = {"sheet":"Sheet", "min_row":2, "min_col":3, "max_col": 7}
        name_cell = "'sheet'!$A$1"
        excel.AddBarChart(x_val_desc_obj, y_val_desc_obj, name_cell)


    excel.Save()





if __name__ == '__main__':
    # TEST_1_colname()
    # TEST_2_change_active_sheet()
    TEST_3_chart()


    
    
    print("Done!")
    
    
    
    pass
