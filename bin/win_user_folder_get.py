#!/usr/bin/python
import argparse
import subprocess
import re
import sys
import os

def WinUserFolderGet( value_name ):
    output = subprocess.check_output(['reg', 'query', r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders', '/v',  value_name])
    match_list = re.findall(r"%s\s+\w+\s+([%%\w: \\\\]*)" % value_name, output)
    return WinEnvVarResolve(match_list[0])

def WinEnvVarResolve( input_str ):
    for item in { x[0] : os.environ.get(x[1],x[0]) for x in re.findall(r"(%([\S^%]*)%)", input_str)}.items():
        input_str = input_str.replace( item[0], item[1])
    return input_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("value_name", nargs='?', type=str, help="ValueName : ex. \"My Pictures\".")
    parser.add_argument("-l", "--list", action="store_true", help="list all ValueName.")

    args = parser.parse_args()

    if(len(sys.argv) == 1):
        parser.print_usage()

    if (args.list):
        output = subprocess.check_output(['reg', 'query', r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' ])
        print output

    if (args.value_name):
        print WinUserFolderGet(args.value_name)


