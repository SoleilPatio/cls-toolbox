#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import argparse
import os
import platform
import glob
import re
import fnmatch
import libPython.core.util as util

"""
-----------------------------------------------
CurrentDirectory() return full path and keep symbolic link remained
-----------------------------------------------
"""
def CurrentDirectory():
    if platform.system() == "Windows":
        cmd = "cd"
    else:
        cmd = "pwd"
    result, stdout, stderr = util.RunCommand(cmd)
    if result != 0:
        util.LogError(f"\n\ncommand={cmd}\n\nresult={result}\n\nstderr={stderr}")
        return os.getcwd()
    return stdout.strip()


def FindFiles( dirpath,  FILE_TYPES, EXCLUDE_DIRS, INCLUDE_DIRS, b_abspath = False):
    cwd = CurrentDirectory()
    # print("cwd=",cwd)
    isabs = os.path.isabs(dirpath)

    append_cwd = False
    if not isabs and b_abspath:
        append_cwd = True
    

    """
    (root, dirnames, filenames) samples:
    ('/python/demo/', ['root'], ['walk.py', 'os_walk.py'])
    ('/python/demo/root', ['3subDir', '2subDir'], ['1file', '3file'])
    ('/python/demo/root/3subDir', [], ['31file'])
    ('/python/demo/root/2subDir', ['22subDir'], ['23file', '21file'])
    ('/python/demo/root/2subDir/22subDir', [], ['221file'])
    """
    count = 0
    for root, dirnames, filenames in os.walk(dirpath):
        if check_if_dir_include( root, EXCLUDE_DIRS, INCLUDE_DIRS) is False:
            continue

        for file_type in FILE_TYPES:
            for filename in fnmatch.filter(filenames, file_type):
                if append_cwd:
                    full_path = os.path.join(cwd, root, filename)
                else:
                    full_path = os.path.join(root, filename)
                print(full_path)
                count += 1

    # print("count=", count)


def check_if_dir_include( path, EXCLUDE_DIRS, INCLUDE_DIRS):
    for in_dir_pattern in INCLUDE_DIRS:
        m = re.match(f".*({in_dir_pattern}).*", path, re.M )
        if m:
            return True
    for ex_dir_pattern in EXCLUDE_DIRS:
        m = re.match(f".*({ex_dir_pattern}).*", path, re.M )
        if m:
            return False
    return True




if __name__ == "__main__":
    parser  = argparse.ArgumentParser(description='Display the full path name of a file.')
    parser.add_argument('vscode_workspace_file', type=str, nargs='?', default=glob.glob('*.code-workspace')[0] if glob.glob('*.code-workspace') else "",
                        help="default use the 1st *.code-workspace in currrent working directory.")
    parser.add_argument('file_filter_config', type=str, nargs='?', default="index_file_filter.conf",
                        help="default use 'index_file_filter.conf' in currrent working directory.")
    parser.add_argument('-a', '--abspath', help="output full absolute path instead of relative one", default=False, action='store_true')
    args = parser.parse_args()

    # print("args.vscode_workspace_file =", args.vscode_workspace_file)
    # print("args.abspath =", args.abspath)

    vscode_prj = util.LoadFromJsonFile(args.vscode_workspace_file)
    vscode_prj_dirs = [ folder["path"] for folder in vscode_prj["folders"] ] 
    # print(vscode_prj_dirs)

    file_filter = util.LoadFromJsonFile(args.file_filter_config)
    FILE_TYPES = file_filter["FILE_TYPES"]
    EXCLUDE_DIRS = file_filter["EXCLUDE_DIRS"]
    INCLUDE_DIRS = file_filter["INCLUDE_DIRS"]

    """
    # TODO: FILE_TYPES, EXCLUDE_DIRS, INCLUDE_DIRS read from config file
    FILE_TYPES = [
        "*.[chxsS]",    "*.aidl",   "*.java",   "*.py",
        "*.cc",         "*.cpp",    "*.cxx",	"*.hpp",    "*.rc",
        "*.dts",	    "*.dtsi",
        "*_defconfig",	"*.mk",	    "*.aidl",	 "*.txt",
        "kconfig",	    "makefile", "README" 
                  ]
    

    if platform.system() == "Windows":
        EXCLUDE_DIRS = [
            r'googletest',
        ]

        INCLUDE_DIRS = [
            r'googletest\\samples',
        ]
    else:
        EXCLUDE_DIRS = [
            # r'googletest/samples',

        ]

        INCLUDE_DIRS = []
    """



    for rel_dir_path in vscode_prj_dirs:
        FindFiles(rel_dir_path, FILE_TYPES, EXCLUDE_DIRS, INCLUDE_DIRS, args.abspath)



    
