#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import argparse
import os
import sys
import platform
import libPython.core.util as util
from fullpath import Fullpath




if __name__ == "__main__":
    print(sys.argv)
    cmd = " ".join(sys.argv[1:])
    print(cmd)
    cmd = "git grep " + cmd
    print(cmd)
    result, stdout, stderr = util.RunCommand(cmd, text_mode = False)
    # result, stdout, stderr = util.RunCommand(cmd, text_mode = True)
    print(result)
    print(stdout)

    stdout = stdout.decode("utf-8") 
    lines = stdout.splitlines()
    for line in lines:
        print(line)


    print(stderr)






    # parser  = argparse.ArgumentParser(description='Display the full path name of a file.')
    # parser.add_argument('filename', type=str, nargs='*', default=[f for f in os.listdir(os.getcwd())],
    #                     help="One or more filenames or directory names. Defaults to all files in the current working directory, like 'ls -a'.")
    # parser.add_argument('-f', '--files-only', help="List only files, not directories", default=False, action='store_true')
    # args = parser.parse_args()

    # for f in args.filename:
    #     full_path = Fullpath(f)
    #     # Print if it's a file, or it's a directory and "--all" is True
    #     if (os.path.isfile(full_path)) or (os.path.isdir(full_path) and not args.files_only):
    #         print(full_path)

