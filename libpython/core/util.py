# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import logging
import pickle
import pathlib
# import json
import commentjson  as json #commentjson cannot be pyinstaller
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
def LogInitial(main_file_path, level=logging.DEBUG):
    #...................................
    #prepare Output directory
    #...................................
    # OUT_DIR = os.path.join( os.getcwd(), "out" )
    OUT_DIR = os.path.join( os.path.dirname(os.path.abspath(main_file_path)) , "out" )
    if not os.path.exists(OUT_DIR):
        try:
            os.makedirs(OUT_DIR)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    #...................................
    #logger 
    #...................................
    exe_log_filename = os.path.join(OUT_DIR, 'execution.log' )
    logging.basicConfig(filename=exe_log_filename, filemode='w', 
        level=logging.DEBUG
        # level=logging.INFO
        )
    
    LogInfo("OUT_DIR= %s" % OUT_DIR)
    LogInfo("exe_log_filename= %s" % exe_log_filename)

    return OUT_DIR

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
    # return json.dumps(obj, indent=4 , sort_keys=True,  ensure_ascii=False)
    #Python 2
    # return json.dumps(obj, indent=4 , sort_keys=True).decode('unicode-escape').encode('utf-8')
    #Python 3
    return json.dumps(obj, indent=4 , sort_keys=True, ensure_ascii=False, default=lambda o: vars(o) ) #ensure_ascii=false for non-ascii character

def _save_to_json_process_(obj):
    try:
        return vars(obj)
    except:
        return f"<<non-serializable: {type(obj).__qualname__}>>"

def SaveToJsonFile(obj, json_file_name, sort_keys=True):
    pathlib.Path(json_file_name).parent.mkdir(parents=True, exist_ok=True)
    with codecs.open(json_file_name, 'w' , encoding='utf-8') as outfile:
        json.dump(obj, outfile, indent=4 , ensure_ascii=False, sort_keys=sort_keys, default=_save_to_json_process_)
        return

def LoadFromJsonFile(json_file_name):
    with codecs.open(json_file_name, 'r' , encoding='utf-8') as infile:
        json_loaded = json.load(infile)
        return json_loaded
                
def SaveToPickleFile(obj, pickle_file_name):
    pathlib.Path(pickle_file_name).parent.mkdir(parents=True, exist_ok=True)
    with open(pickle_file_name, 'wb') as outfile:
        pickle.dump(obj, outfile, protocol=pickle.HIGHEST_PROTOCOL)
        return

def LoadFromPickleFile(pickle_file_name):
    with open(pickle_file_name, 'rb') as infile:
        pickle_loaded = pickle.load(infile)
        return pickle_loaded



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

def LoadPythonModule( python_src_file ):
    py_src = pathlib.Path(python_src_file)
    sys.path.append(str(py_src.parent))    #add module directory to  path
    module_name = py_src.stem
    module = importlib.import_module(module_name)
    return module

def SaveToProperPltfig(plt, ref_file_name):
    out_jpg_file_name = pathlib.Path(ref_file_name).parent / "out" /  ( pathlib.Path(ref_file_name).stem + "_out.jpg" )
    pathlib.Path(out_jpg_file_name).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig( out_jpg_file_name)
    msg = "jpg saved: %s" % out_jpg_file_name
    print(msg)
    logging.info(msg)

def SaveToProperPickle(obj, ref_file_name):
    out_pickle_file_name = pathlib.Path(ref_file_name).parent / "out" /  ( pathlib.Path(ref_file_name).stem + "_out.pickle" )
    pathlib.Path(out_pickle_file_name).parent.mkdir(parents=True, exist_ok=True)
    SaveToPickleFile( obj, out_pickle_file_name )
    msg = "pickle saved: %s" % out_pickle_file_name
    print(msg)
    logging.info(msg)

"""
-----------------------------------------------
Find the nearest specific file, usually setting file
-----------------------------------------------
"""

def FindNearestFile( start_position, file_name ):
    import os
    from pathlib import Path

    start_position = os.path.abspath(start_position)
    parents = [ str(x) for x in Path(start_position).parents ]

    # LogInfo("start_position = %s" % start_position)
    for path in parents:
        test_file_name = os.path.join(path, file_name)
        # LogInfo("test_file_name = %s" % test_file_name)
        if os.path.isfile(test_file_name):
            LogInfo("file found: %s" % test_file_name)
            return test_file_name
    return None


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

    SaveToJsonFile(data, "test.json" )

    data2 = LoadFromJsonFile("test.json")
    print("data2=", StrObj(data2))

