#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from libPython.Utils.DayCode import DayCode


def list_all_files(ret_files, dirname, ext_list, b_recursive ):
    ext_list = [ ext.lower() for ext in ext_list ]
    for root, dirs, files in os.walk(dirname):
        # print("root: " + root)
        # print("dirs: " + str(dirs) )
        # print("files: " + str(files))
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext.lower()[1:] in ext_list:
                ret_files.append(os.path.join(root, f))
        if not b_recursive: #Assume the 1st iteration is the root directory
            break



def check_file_status(filename):
    '''
    :param filename:
    :rtype dict{
            "stat_result": os.stat(), 
            "day_code_atime":...
            }
    '''

    if os.path.isfile(filename) != True:
        return None
    
    ret = {}
    
    stat_result = os.stat(filename)
    ret["stat_result"] = stat_result
    
    #Process Time
    """
    :day_code_atime: access time
    :day_code_mtime: modified time
    :day_code_ctime: create time
    """
    ret["day_code_atime"] = DayCode().set_from_epoch_sec(stat_result.st_atime).to_yyyymmddHHMM()
    ret["day_code_mtime"] = DayCode().set_from_epoch_sec(stat_result.st_mtime).to_yyyymmddHHMM()
    ret["day_code_ctime"] = DayCode().set_from_epoch_sec(stat_result.st_ctime).to_yyyymmddHHMM()
    
    
    #Process Filename
    """
    :filename: c:\\dir_1\\dir_2\\foo.exe
    :fn_basename: foo.exe
    :fn_dirname: c:\\dir_1\\dir_2
    :fn_parent_dirname: dir_2
    :fn_noext: foo
    :fn_ext: .exe
    :fn_abs_dirname: c:
    :fn_abs_dirname_nodrive: \\dir_1\\dir_2
    """
    ret["fn_basename"] = os.path.basename(filename)
    ret["fn_dirname"] = os.path.dirname(filename)
    ret["fn_parent_dirname"] = os.path.basename(ret["fn_dirname"])
    ret["fn_noext"] = os.path.splitext(ret["fn_basename"])[0]
    ret["fn_ext"] = os.path.splitext(ret["fn_basename"])[1]
    
    ret["fn_abs_filename"] = os.path.abspath(filename)
    ret["fn_abs_dirname"] = os.path.dirname(ret["fn_abs_filename"])
    
    ret["fn_drive"] = os.path.splitdrive(ret["fn_abs_dirname"])[0]
    ret["fn_abs_dirname_nodrive"] = os.path.splitdrive(ret["fn_abs_dirname"])[1]
    
    
    return ret
        



if __name__ == "__main__":
    ret = check_file_status(r"N:\project\my-mtk-code\regression-engine\resource\bit_field_definition.xlsx")
    print(ret)
    
    print( ret["fn_abs_dirname"] )
    print( type(ret["fn_abs_dirname"]) )
    
    print( os.path.join("_cache", ret["fn_abs_dirname"] , ret["fn_basename"]) )
    
    
    print( "\nDone" )