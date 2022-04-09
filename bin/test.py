#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )

import argparse
import os
import sys
import platform

if __name__ == "__main__":
    print("======= Environment Variables =======")
    os.environ["CLS_PYTHON"] = "hihi!bless you!"
    for ii in os.environ.items():
        print(ii)
    print("")

#...................................
#
#...................................
    print("======= Arguments =======")
    print("sys.argv = ", sys.argv )
    print("os.name = ", os.name )
    print("platform.system = ", platform.system() )
    print("platform.release = ", platform.release() )

    exit(0)
 