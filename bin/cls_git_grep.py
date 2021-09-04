#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__': import _libpythonpath_ #type: ignore (Add libPython\.. into PYTHONPATH when unittest )


import sys
import re
import libPython.core.util as util
from fullpath import Fullpath



if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:])
    cmd = "git grep -n " + cmd
    print("command: ", cmd)
    print("")

    result, stdout, stderr = util.RunCommand(cmd, text_mode = False)
    # result, stdout, stderr = util.RunCommand(cmd, text_mode = True)
    if result != 0:
        stderr = stderr.decode("utf-8")
        util.LogError(f"\n\nresult={result}\n\nstderr={stderr}")
        exit(-1)

    stdout = stdout.decode("utf-8") 
    lines = stdout.splitlines()
    for line in lines:
        """
        algorithm/cracking_the_coding_interview_5/python/Phase1/bit_manipulation.py-52-
        algorithm/cracking_the_coding_interview_5/python/Phase1/bit_manipulation.py:53:def main_float_to_bin():
        algorithm/cracking_the_coding_interview_5/python/Phase1/bit_manipulation.py-54-    print float_to_bin(0.5)
        """
        m = re.match( r"(.*)([:-]\d+[:-].*)", line, re.M)
        if m:
            fullpath = Fullpath(m.group(1))
            line = fullpath + m.group(2)
        print(line)

