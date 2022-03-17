# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import logging
import pickle
import pathlib
try:
    import commentjson  as json #commentjson cannot be pyinstaller
except:
    import json
    print("[WARN] no 'commentjson' module installed, use 'json' module instead.")
import codecs
import subprocess
import shlex
import traceback
import errno
import importlib
import bisect
import inspect



"""
-----------------------------------------------
Exception
-----------------------------------------------
"""
def ExceptionStr():
        return traceback.format_exc() 

"""
-----------------------------------------------
Log Utilities
    base_path:
        file: create out at the same level
        dir : create out under it
-----------------------------------------------
"""
def LogInitial(base_path, level=logging.DEBUG, prog_name="", format_no=0):
    #...................................
    #prepare Output directory
    #...................................
    rootdir = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
    OUT_DIR = os.path.join( rootdir, "out-" + prog_name  if prog_name else "out" )
    if not os.path.exists(OUT_DIR):
        CreateDir(OUT_DIR)
    #...................................
    #logger 
    #...................................
    exe_log_filename = os.path.join(OUT_DIR, f'log-execution-{prog_name}.log' if prog_name else 'log-execution.log' )
    
    if format_no == 0:
        logging.basicConfig(filename=exe_log_filename, filemode='w', 
            level=level
            # level=logging.INFO
            )
    else:
        format = {
            1: "%(asctime)s [%(levelname)s] %(message)s"
        }

        datefmt = {
            1: "%Y-%m-%d %H:%M:%S"
        }

        logging.basicConfig(filename=exe_log_filename, filemode='w', 
            level=level,
            format = format[format_no], datefmt = datefmt[format_no]
            )


    LogInfo("OUT_DIR= %s" % OUT_DIR, stdout=False)
    LogInfo("exe_log_filename= %s" % exe_log_filename, stdout=False)
    return OUT_DIR, exe_log_filename

def Log( msg, stdout = True ):
    func = inspect.currentframe().f_back.f_code
    msg = f"{func.co_name}:{msg}"
    print(msg) if stdout else None
    logging.info(msg)

def LogInfo( msg, stdout = True  ):
    func = inspect.currentframe().f_back.f_code
    msg = f"{func.co_name}:{msg}"
    print("[INFO]", msg) if stdout else None
    logging.info(msg)

def LogWarning( msg, stdout = True  ):
    func = inspect.currentframe().f_back.f_code
    msg = f"{func.co_name}:{msg}"
    print("[WARN]", msg) if stdout else None
    logging.warning(msg)

def LogError( msg, stdout = True  ):
    func = inspect.currentframe().f_back.f_code
    msg = f"{func.co_name}:{msg}"
    print("[ERROR]", msg) if stdout else None
    logging.error(msg)


"""
--------------------------------------------------------
Printable/Readable/Loadable Utilities
--------------------------------------------------------
"""
def _save_to_json_process_(obj):
    try:
        return vars(obj)
    except:
        return f"<<non-serializable: {type(obj).__qualname__}>>"

def StrObj(obj, sort_keys=True):
    return json.dumps(obj, indent=4 , ensure_ascii=False, sort_keys=sort_keys,  default=_save_to_json_process_ ) #ensure_ascii=false for non-ascii character


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
--------------------------------------------------------
List/Array Utilities
--------------------------------------------------------
"""
"""
-----------------------------------------------
ListFindRangeIdx:
    input_list[lo_i:up_i] is what you want
-----------------------------------------------
"""
def ListFindRangeIdx( input_list, min_value = float('-inf'), max_value = float('inf')):
    lo_i=bisect.bisect_left(input_list, min_value)
    up_i=bisect.bisect_right(input_list, max_value, lo=lo_i)
    return (lo_i, up_i)




    
"""
--------------------------------------------------------
Save Proper Utilities
--------------------------------------------------------
"""
def SaveToProperJson(obj, ref_file_name, tag=""):
    out_json_file_name = pathlib.Path(ref_file_name).parent / "out" /  ( pathlib.Path(ref_file_name).stem + tag + "_out.json" )
    pathlib.Path(out_json_file_name).parent.mkdir(parents=True, exist_ok=True)
    SaveToJsonFile( obj, out_json_file_name )
    msg = "json saved: %s" % out_json_file_name
    LogInfo(msg)

def SaveToProperPickle(obj, ref_file_name, tag=""):
    out_pickle_file_name = pathlib.Path(ref_file_name).parent / "out" /  ( pathlib.Path(ref_file_name).stem + tag + "_out.pickle" )
    pathlib.Path(out_pickle_file_name).parent.mkdir(parents=True, exist_ok=True)
    SaveToPickleFile( obj, out_pickle_file_name )
    msg = "pickle saved: %s" % out_pickle_file_name
    LogInfo(msg)

def SaveToProperPltfig(plt, ref_file_name, tag=""):
    out_jpg_file_name = pathlib.Path(ref_file_name).parent / "out" /  ( pathlib.Path(ref_file_name).stem + tag + "_out.jpg" )
    pathlib.Path(out_jpg_file_name).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig( out_jpg_file_name)
    msg = "jpg saved: %s" % out_jpg_file_name
    LogInfo(msg)


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
Execute Command Utilities
    text_mode : True  => text mode , under linux
                False => UTF-8 mode, under windows

    [?] if you force text mode, sometimes app output characters that cannot be processed, get index error : "stdout = stdout[0] IndexError: list index out of range"

    if <class 'str'> just return
    if <class 'bytes'> try decode utf-8 , then cp950
-----------------------------------------------
"""
def RunCommand( command_line, input_str = None, text_mode = False ):
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

    if text_mode:
        return (ret_code, std_out, std_err)
    else:
        try:
            return (ret_code, std_out.decode("utf-8"), std_err.decode("utf-8"))
        except:
            try:
                return (ret_code, std_out.decode("big5"), std_err.decode("big5"))
            except:
                return (ret_code, str(std_out), str(std_err))


"""
-----------------------------------------------
Execute Command Utilities Synchronize

-----------------------------------------------
"""
def RunCommandSync( command_line):
    #........................................................
    # Execute command line
    #........................................................
    return subprocess.run(shlex.split(command_line))


"""
-----------------------------------------------
Load Python Module
-----------------------------------------------
"""
def LoadPythonModule( python_src_file ):
    py_src = pathlib.Path(python_src_file)
    sys.path.append(str(py_src.parent))    #add module directory to  path
    module_name = py_src.stem
    module = importlib.import_module(module_name)
    return module


"""
-----------------------------------------------
Find the nearest specific file, usually setting file
-----------------------------------------------
"""
def FindNearestFile( start_position, file_name ):
    start_position = os.path.abspath(start_position)
    parents = [ str(x) for x in pathlib.Path(start_position).parents ]

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
    import wx #type: ignore
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
    import wx #type: ignore
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
    LogInitial(__file__, format_no=1)
    LogInfo("Test")
