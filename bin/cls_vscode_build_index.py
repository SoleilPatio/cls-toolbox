#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import argparse
import os
import platform
import libPython.core.util as util
import glob

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


def FindFiles( dirpath,  FILE_TYPES):
    cwd = CurrentDirectory()
    print("cwd=",cwd)
    print("os.getcwd()=", os.getcwd())
    # os.chdir(rel_dirpath)
    print("rel_dirpath=", dirpath)
    # print("os.getcwd()=", os.getcwd())

    import fnmatch

    matches = []
    for root, dirnames, filenames in os.walk(dirpath):
        for file_type in FILE_TYPES:
            for filename in fnmatch.filter(filenames, file_type):
                matches.append(os.path.join(root, filename))

    for file in matches:
        print(file)
    print("count=", len(matches))


if __name__ == "__main__":
    parser  = argparse.ArgumentParser(description='Display the full path name of a file.')
    parser.add_argument('vscode_workspace_file', type=str, nargs='?', default=glob.glob('*.code-workspace')[0] if glob.glob('*.code-workspace') else "",
                        help="default use the 1st *.code-workspace in currrent working directory.")
    # parser.add_argument('-f', '--files-only', help="List only files, not directories", default=False, action='store_true')
    args = parser.parse_args()

    print("args.vscode_workspace_file =", args.vscode_workspace_file)

    vscode_prj = util.LoadFromJsonFile(args.vscode_workspace_file)
    vscode_prj_dirs = [ folder["path"] for folder in vscode_prj["folders"] ] 
    print(vscode_prj_dirs)

    FILE_TYPES = [
        "*.[chxsS]",    "*.aidl",   "*.java",   "*.py",
        "*.cc",         "*.cpp",    "*.cxx",	"*.hpp",    "*.rc",
        "*.dts",	    "*.dtsi",
        "*_defconfig",	"*.mk",	    "*.aidl",	 "*.txt",
        "kconfig",	    "makefile", "README" 
                  ]


    for rel_dir_path in vscode_prj_dirs:
        FindFiles(rel_dir_path, FILE_TYPES)



    
