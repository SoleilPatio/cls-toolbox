'''
@author: clouds
'''

import xlwings as xw
from clsobject import clsobject

class clsXlwingsFile(clsobject):
    def __init__(self):
        self.book = None
        pass
    
    def Open(self, filename):
        self.book = xw.Book(filename)
        
    def ListOpenExcelFiles(self):
        ret = []
        for i, app in enumerate(xw.apps):
            print "app",i,":"
            for book in app.books:
                print "\t",book.name
                ret.append(book.name)
        return ret
                
    def ListSheets(self):
        ret = []
        for sheet in self.book.sheets:
            print sheet.name
            ret.append(sheet.name)
        return ret
            
    def GetSheetByName(self, sheet_name):
        for sheet in self.book.sheets:
            if sheet_name == sheet.name:
                return sheet
        return None
    
    def GetSheetByIndex(self, index):
        return self.book.sheets[index]
    
    def LastRowOfSheet(self, sheet_obj):
        return sheet_obj.cells(65536,1).end("up").row
    
    def ParseSheetAsTable(self, sheet_obj):
        ret_table = []
        
        field_names = sheet_obj.range("A1").expand("right").value
        
        max_row = self.LastRowOfSheet(sheet_obj)
        max_col = len(field_names)
        print "rowcount=", max_row
        print "colcount=", max_col
        
        
        records = sheet_obj.range(xw.Range("A2"),(max_row,max_col)).value
        print field_names
        
        for i, record in enumerate(records):
            r_dict = {}
            for j, value in enumerate(record):
                r_dict[field_names[j]] = value
            ret_table.append(r_dict)
            
        return ret_table
            
        
        
        
        


if __name__ == '__main__':
    filename = r"D:\Users\clouds\Desktop\contacts.csv"
    filename = r"D:\Project-D\TASKs\coda_parser.task\Rocky_cam_a_000_ctl.xls"
    filename = r"D:\Project-D\TASKs\coda_parser.task\Cannon_CODA\CODA\Cannon_DISP_SPLIT_CODA.xls"
    
    xwobj = clsXlwingsFile()
    
    xwobj.Open(filename)
    xwobj.ListOpenExcelFiles()
    xwobj.ListSheets()
    
    sheet = xwobj.GetSheetByIndex(0)
    
    print sheet.name
    
    print "last row of ", sheet.name, " is ",  xwobj.LastRowOfSheet(sheet)
    
    table = xwobj.ParseSheetAsTable(sheet)
    
    for r in table:
        print r
    
    
    
    
    pass