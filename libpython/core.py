# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import logging
import json
# import commentjson  as json #commentjson cannot be pyinstaller
import codecs
import subprocess
import traceback
import errno


"""
-----------------------------------------------

-----------------------------------------------
"""
def ExceptionStr(self):
        return traceback.format_exc() 

"""
-----------------------------------------------
Log utility
-----------------------------------------------
"""
def Log( msg, stdout = True ):
    print(msg) if stdout else None
    logging.info(msg)

def LogInfo( msg, stdout = True  ):
    print("[INFO]", msg) if stdout else None
    logging.info(msg)

def LogWarning( msg, stdout = True  ):
    print("[WARN]", msg) if stdout else None
    logging.warning(msg)

def LogError( msg, stdout = True  ):
    print("[ERROR]", msg) if stdout else None
    logging.error(msg)


"""
--------------------------------------------------------
Return printable string of ANY object
    1. support URF-8 key name
--------------------------------------------------------
"""
def StrObj(obj):
    #........................................................
    # sometimes error: 
    #           UnicodeEncodeError: 'ascii' codec can't encode characters in position 7-8: ordinal not in range(128)
    #........................................................
    # return json.dumps(obj, indent=4 , sort_keys=True).decode('unicode-escape')

    #........................................................
    # encode to utf-8 before output for print.
    # ensure_ascii=False : no \u for utf-8
    #........................................................
    # return json.dumps(obj, indent=4 , sort_keys=True).decode('unicode-escape').encode('utf-8')
    return json.dumps(obj, indent=4 , sort_keys=True,  ensure_ascii=False)

"""
--------------------------------------------------------
Save ANY object to json
--------------------------------------------------------
"""
def SaveObjToJson(obj, json_file_name):
    with codecs.open(json_file_name, 'w' , encoding='utf-8') as outfile:
        json.dump(obj, outfile, indent=4 , ensure_ascii=False, sort_keys=True)

"""
--------------------------------------------------------
Load ANY object from json
--------------------------------------------------------
"""
def LoadObjFromJson(json_file_name):
    with open(json_file_name) as infile:
        obj = json.load(infile)
    return obj



"""
-----------------------------------------------
Create OUT directory
-----------------------------------------------
"""

def CreateDir( dir_name):
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return dir_name

def CreateDefaultOutDir( self, out_dir="out"):
    OUT_DIR = os.path.join( os.getcwd(), out_dir )
    return CreateDir(OUT_DIR)


"""
-----------------------------------------------
Execute Command
    text_mode : True  => text mode , under linux
                False => UTF-8 mode, under windows
-----------------------------------------------
"""
def RunCommand( command_line, input_str = None, text_mode = True ):
    #........................................................
    # Execute command line
    #........................................................
    cmd_str = command_line
    if input_str:
        output = subprocess.Popen( cmd_str, shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=text_mode) #[NOTE]: text=True, text mode
        std_out, std_err = output.communicate(input=input_str)
        
    else:
        output = subprocess.Popen( cmd_str, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=text_mode) #[NOTE]: text=True, text mode
        std_out, std_err = output.communicate()
    
    ret_code = output.returncode
    return (ret_code, std_out, std_err)



"""
========================================================
WxPython Windows Utilities
========================================================
"""
"""
--------------------------------------------------------
WxWidgetDataSync:
    direction:
            'to'  : ==>  (restore operation)
            'from': <==  (read operation)
    dic_obj[key] <==>  widget
--------------------------------------------------------
"""
def WxWidgetDataSync( dic_obj, key, widget , direction='from'):
    #Read value from GUI widget
    if direction == 'from':
        dic_obj[key] = WxGetWidgetValue(widget)
    elif direction == 'to':
        WxSetWidgetValue(widget, dic_obj[key])
    else:
        logging.error("invaild direction: %s"%direction)
        assert False



def WxGetWidgetValue(widget):
    import wx
    if      isinstance(widget, wx.ComboBox):    #https://wxpython.org/Phoenix/docs/html/wx.ComboBox.html?highlight=wx%20combobox#wx.ComboBox
        return widget.GetValue()
        # return widget.GetStringSelection()
    elif    isinstance(widget, wx.SpinCtrl):    #https://wxpython.org/Phoenix/docs/html/wx.SpinCtrl.html?highlight=wx%20spinctrl#wx.SpinCtrl 
        return widget.GetValue()
    elif    isinstance(widget, wx.SpinCtrlDouble):  #https://wxpython.org/Phoenix/docs/html/wx.SpinCtrlDouble.html?highlight=spinctrldouble#wx.SpinCtrlDouble 
        return widget.GetValue()
    else:
        logging.error("Unsupport WX widget: %s"%type(widget))

  
  

def WxSetWidgetValue(widget, value):
    import wx
    if      isinstance(widget, wx.ComboBox):    #https://wxpython.org/Phoenix/docs/html/wx.ComboBox.html?highlight=wx%20combobox#wx.ComboBox
        return widget.SetValue(str(value))
    elif    isinstance(widget, wx.SpinCtrl):    #https://wxpython.org/Phoenix/docs/html/wx.SpinCtrl.html?highlight=wx%20spinctrl#wx.SpinCtrl 
        return widget.SetValue(value)
    elif    isinstance(widget, wx.SpinCtrlDouble):  #https://wxpython.org/Phoenix/docs/html/wx.SpinCtrlDouble.html?highlight=spinctrldouble#wx.SpinCtrlDouble 
        return widget.SetValue(value)
    else:
        logging.error("Unsupport WX widget: %s"%type(widget))




"""
--------------------------------------------------------
Main Test
--------------------------------------------------------
"""
if __name__ == '__main__':
    data = [u"中文",u"好棒棒"]
    print("data=", StrObj(data))

    SaveObjToJson(data, "test.json" )

    data2 = LoadObjFromJson("test.json")
    print("data2=", StrObj(data2))

