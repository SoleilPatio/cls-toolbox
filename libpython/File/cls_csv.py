'''
@author: clouds
'''
import csv
from clsobject import clsobject

class clsCsv(clsobject):
    def __init__(self):
        self.rows = []
        pass
    
    def Open(self, filename):
        self.rows = []
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                self.rows.append(row)
        
    def ListOpenExcelFiles(self):
        pass
                 
    def ListSheets(self):
        pass
             
    def GetSheetByName(self, sheet_name):
        pass
     
    def GetSheetByIndex(self, index):
        pass
     
    def LastRowOfSheet(self, sheet_obj = None):
        return len(self.rows)
     
    """
    cascade_field_name: if field_name_row_num is > 0, want to cascade filed name from 0-field_name_row_num ?
    pass_down_field_names: if current cell do not have value, use value in upper cell
    """
    
    def ParseSheetAsTable(self, sheet_obj, field_name_row_num = 0, cascade_field_name = True, pass_down_field_names = [], lower_case_field_name = False):
        pass
    
    
    def GetSheetCol(self, col_num, sheet_obj = None):
        return [ row[col_num]  for row in self.rows ]
        
            


if __name__ == '__main__':
    
    filename = r"D:\Project\tyche\data\yloader\usa\HIMX.csv"
    
    csvobj = clsCsv()
    
    csvobj.Open(filename)
    
    print csvobj.LastRowOfSheet()
    
    timestamp = csvobj.GetSheetCol(0)
    
    
        
    
    
#     print len(csvobj.GetSheetCol(1))
#     print len(csvobj.GetSheetCol(2))
#     print len(csvobj.GetSheetCol(3))
#     print len(csvobj.GetSheetCol(4))
#     print len(csvobj.GetSheetCol(5))
#     print csvobj.GetSheetCol(6)
    
    
    
    