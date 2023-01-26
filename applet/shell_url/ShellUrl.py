#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
#................................................................................
# Add libPython\.. into PYTHONPATH
import sys
#sys.path.append(r'N:\bin\cls-toolbox')
#sys.path.append(r'D:\PROJECT\semu-toolbox\met-logx-ex')
#................................................................................
# cls-url:god bless you

import os
import logging
import urllib.parse
import subprocess
import shlex

logging.basicConfig(filename=r"d:\\out-shell_url.log", filemode='w', 
            level=logging.DEBUG
            # level=logging.INFO
            )


if __name__ == "__main__":
    logging.info("cwd=" + os.getcwd())
    logging.info("argv=" + str(sys.argv))
    unquote_str = urllib.parse.unquote(sys.argv[1][len("shell-url://"):]).rstrip("/")
    logging.info("unquote_str(striped)=" + unquote_str)


    if os.path.isdir(unquote_str) is True:
        command_line = f'explorer "{unquote_str}"'
    else:
        command_line = unquote_str
    
    logging.info("command_line=" + command_line)

    
    # ret = subprocess.run(shlex.split(command_line))
    # ret = subprocess.run(command_line)
    ret = subprocess.call(command_line, shell=True) #no return?but can be delete log file
    # ret = os.startfile(command_line) #no return?but can be delete log file
    logging.info("ret=" + ret)

    logging.info("done")

