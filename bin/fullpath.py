#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import argparse
import os
import platform
import libPython.core.util as util

def Fullpath( filename ):
    if platform.system() == "Windows":
        cmd = "cd"
    else:
        cmd = "pwd"
    result, stdout, stderr = util.RunCommand(cmd)
    if result != 0:
        util.LogError(f"file={f}\n\ncommand={cmd}\n\nresult={result}\n\nstderr={stderr}")
        return filename
    full_path = os.path.join(stdout.strip(), filename)
    return full_path


if __name__ == "__main__":
    parser  = argparse.ArgumentParser(description='Display the full path name of a file.')
    parser.add_argument('filename', type=str, nargs='*', default=[f for f in os.listdir(os.getcwd())],
                        help="One or more filenames or directory names. Defaults to all files in the current working directory, like 'ls -a'.")
    parser.add_argument('-f', '--files-only', help="List only files, not directories", default=False, action='store_true')
    args = parser.parse_args()

    for f in args.filename:
        full_path = Fullpath(f)
        # Print if it's a file, or it's a directory and "--all" is True
        if (os.path.isfile(full_path)) or (os.path.isdir(full_path) and not args.files_only):
            print(full_path)

