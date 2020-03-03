# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import File.cls_xlwings as clsxw
import re
from clsobject import clsobject

class ContactGroup(clsobject):
    def __init__(self):
        self.value = None
        self.favor = None
        self.contacts = []
        
        

def SearchValue(content_str, key):
    match_str = key+"\s*:\s*(.*)"
    matchObj = re.search( match_str, content_str, re.M|re.I)
    if matchObj:
        return matchObj.group(1)
    return None


def CreateContactGroupByCoordinate(table):
    
    ret_list = []
    pair_dict = {}
    
    for r in table:
        def _to_str(x):
            if x is None:
                return ""
            return x if isinstance(x, (str, unicode)) else str(x)
        
        name = _to_str(r["First Name"]) + _to_str(r["Middle Name"]) + _to_str(r["Last Name"])
        if name == "":
            continue
            
        note = r["Notes"]
        if note is None:
            continue
        
        
        
        value = SearchValue(note, "Value")
        favor = SearchValue(note, "Favor")
        
        try:
            value = float(value) if value is not None else None
            favor = float(favor) if favor is not None else None
            
        except:
            print name, "has error!"
            continue
        
        
        if (favor is None and value is not None) or (favor is not None and value is None):
            print name, "has only one valid index"
        
        if value is not None and favor is not None:
            print name, "(%f,%f)"%(value,favor)
            
            #Add to dict
            if (value,favor) not in pair_dict:
                pair_dict[(value,favor)] = ContactGroup()
                pair_dict[(value,favor)].value = value
                pair_dict[(value,favor)].favor = favor
                
            pair_dict[(value,favor)].contacts.append(name)
            
                    
    #Prepare return list
    for pair in sorted(pair_dict, reverse = True):
        ret_list.append(pair_dict[pair])
        
    return ret_list


def PlotContactGroups(contact_groups):
    import numpy as np
    
    #Draw Axis
    plt.plot([1,5],[3,3],alpha=0.2) #x-axis
    plt.plot([3,3],[1,5],alpha=0.2)
    
    x = [ c.favor for c in contact_groups ]
    y = [ c.value for c in contact_groups ]
    s = [ 50*len(c.contacts) for c in contact_groups ]

    colors = np.random.rand(len(x))
    
    #Show dot
    plt.scatter(x, y, s, colors, alpha=0.5)
    
    #Show Name
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    
    for i,cg in enumerate(contact_groups):
        size=9
        color= "black"
        weight= "normal"
        style = "normal"
        rotation = 0
        
        cg.value 
        if   2 < cg.value < 4:
            color = "0.3"
        elif 1 < cg.value <= 2:
            color = "0.5"
        elif cg.value <= 1:
            color = "0.8"
            
        plt.text(cg.favor, cg.value, "\n".join(cg.contacts), 
                 size=size, color=color, 
                 weight  = weight ,
                 style = style,
                 rotation = rotation,
                 ha='center', va='center', 
                 wrap=True)
        
    
    
    
    plt.show()
    
            
    
        
    
    

if __name__ == "__main__":
    """
    [CLS]:Input is export from google contact in outlook csv format
    Value:3
    Favor:3
    
    Value:(正向力量  or 資訊情報來源)
    1: 妖魔鬼怪
    2: 賠錢貨
    3: 沒有幫助
    4: 有價值
    5. 非常有價值
    
    Favor:
    1: 非常討厭
    2: 保持距離
    3: 正常相處
    4: 喜歡相處
    5: 非常喜歡相處
    """
    
    EXCEL_FILE_NAME = r"D:\Users\clouds\Desktop\contacts.csv"
    
    clsxwfile = clsxw.clsXlwingsFile()
    clsxwfile.Open(EXCEL_FILE_NAME)
    
    sheet = clsxwfile.GetSheetByIndex(0)
    table = clsxwfile.ParseSheetAsTable(sheet)
    
    contact_groups = CreateContactGroupByCoordinate(table)
    
    
    PlotContactGroups(contact_groups)
    
    
    print "Done"