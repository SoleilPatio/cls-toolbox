#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import argparse
import os
import platform
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


def FindFiles( dirpath,  FILE_TYPES, EXCLUDE_DIR_PATTERN, INCLUDE_DIR_PATTERN, b_abspath = False):
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
    dir_exclude_count = 0
    file_count = 0
    file_type_count = { file_type:0 for file_type in FILE_TYPES }
    for root, dirnames, filenames in os.walk(dirpath):
        if check_if_dir_include( root, EXCLUDE_DIR_PATTERN, INCLUDE_DIR_PATTERN) is False:
            dir_exclude_count +=1
            continue

        for file_type in FILE_TYPES:
            for filename in fnmatch.filter(filenames, file_type):
                if append_cwd:
                    full_path = os.path.join(cwd, root, filename)
                else:
                    full_path = os.path.join(root, filename)
                print(full_path)
                file_count += 1
                file_type_count[file_type] += 1

    util.LogInfo(f"\tfile_count={file_count}", stdout=False)
    util.LogInfo(f"\tdir_exclude_count={dir_exclude_count}", stdout=False)
    for file_type in FILE_TYPES:
        if file_type_count[file_type]:
            util.LogInfo(f"\t\tfile_type[{file_type}]={file_type_count[file_type]}", stdout=False)


def check_if_dir_include( path, EXCLUDE_DIR_PATTERN, INCLUDE_DIR_PATTERN):
    for in_dir_pattern in INCLUDE_DIR_PATTERN:
        m = re.match(f".*({in_dir_pattern}).*", path, re.M )
        if m:
            return True
    for ex_dir_pattern in EXCLUDE_DIR_PATTERN:
        m = re.match(f".*({ex_dir_pattern}).*", path, re.M )
        if m:
            return False
    return True




if __name__ == "__main__":
    print(os.getcwd())
    util.LogInitial(os.getcwd(), prog_name="cls_cscope_find")

    parser  = argparse.ArgumentParser(description='"find" utility for cscope index use.')
    # parser.add_argument('vscode_workspace_file', type=str, nargs='?', default=glob.glob('*.code-workspace')[0] if glob.glob('*.code-workspace') else "",
    #                     help="default use the 1st *.code-workspace in currrent working directory.")
    parser.add_argument('config_file', type=str, nargs='?', default="cls_cscope_find.conf",
                        help="default use 'cls_cscope_find.conf' in currrent working directory.")
    parser.add_argument('-a', '--abspath', help="output full absolute path instead of relative one", default=False, action='store_true')
    args = parser.parse_args()

    util.LogInfo(f"args.abspath={args.abspath}", stdout=False )


    config = util.LoadFromJsonFile(args.config_file)
    FILE_TYPES =    config.get("FILE_TYPES", ["*.*"])  # default *.*
    PROJECTS =      config.get("PROJECTS", {".":{}} )    # default current directory

    for project_dir in PROJECTS.keys():
        
        EXCLUDE_DIR_PATTERN = PROJECTS[project_dir].get("EXCLUDE_DIR_PATTERN", [])
        INCLUDE_DIR_PATTERN = PROJECTS[project_dir].get("INCLUDE_DIR_PATTERN", [])

        util.LogInfo(f"project_dir={project_dir}", stdout=False)
        util.LogInfo(f"\tEXCLUDE_DIR_PATTERN={EXCLUDE_DIR_PATTERN}", stdout=False)
        util.LogInfo(f"\tINCLUDE_DIR_PATTERN={INCLUDE_DIR_PATTERN}", stdout=False)


        FindFiles(project_dir, FILE_TYPES, EXCLUDE_DIR_PATTERN, INCLUDE_DIR_PATTERN, args.abspath)



    
