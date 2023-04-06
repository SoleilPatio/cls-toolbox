#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
#------------------------------------------------------------------------------
if __name__ == "__main__": import _libpythonpath_ # Add libPython\.. into PYTHONPATH when unittest
#------------------------------------------------------------------------------
import libPython.core.util as util
# import libPython.core.util_ex as util_ex


import logging
import os

class FtraceLog():
    def __init__(self, prog_name=""):
        self.m_prog_name = prog_name
        self.m_logger = logging.getLogger("ftrace")
        self.m_logger.setLevel(logging.DEBUG)
        self.m_pid = os.getpid()

        pass

    def LogInitial(self, base_path, prog_name=""):
        #...................................
        #prepare Output directory
        #...................................
        rootdir = base_path if os.path.isdir(base_path) else os.path.dirname(base_path)
        OUT_DIR = os.path.join( rootdir, "out-" + self.m_prog_name  if self.m_prog_name else "out" )
        if not os.path.exists(OUT_DIR):
            util.CreateDir(OUT_DIR)
        #...................................
        #ftrace file 
        #...................................
        exe_log_filename = os.path.join(OUT_DIR, f'log-ftrace-{prog_name}.log' if prog_name else 'log-ftrace.log' )


        # console handlers
        stream_handler = logging.StreamHandler()  # Handler for the logger
        stream_handler.setLevel(logging.DEBUG)
        self.m_logger.addHandler(stream_handler) #seems only apply to "console" logging format

        # file handlers
        file_handler = logging.FileHandler(filename=exe_log_filename, mode='w')  # Handler for the logger
        file_handler.setLevel(logging.DEBUG)
        self.m_logger.addHandler(file_handler)


        #...................................
        # add ftrace log file header "# tracer: nop"
        #...................................
        # First, generic formatter:
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.m_logger.error("# tracer: nop")

        #...................................
        # ftrace log format
        #...................................
        #restore format:
        # FTRACE_FMT = "FTRACELOG-0 [0] ...1 %(asctime)s.%(msecs)03d: tracing_mark_write: %(message)s"
        # FTRACE_FMT = "FTRACELOG-0 [0] ...1 %(asctime)s.%(msecs)03d: %(message)s"
        FTRACE_FMT = "FTRACELOG-%(thread)d [0] ...1 %(created)f: %(message)s"
        
        stream_handler.setFormatter( logging.Formatter(fmt=FTRACE_FMT, datefmt="%S") )
        file_handler.setFormatter( logging.Formatter(fmt=FTRACE_FMT, datefmt="%S") )

        return OUT_DIR, exe_log_filename
    
    def atrace_B(self, functionname ):
        self.m_logger.error(f"tracing_mark_write: B|{self.m_pid}|{functionname}")

    def atrace_E(self):
        self.m_logger.error("tracing_mark_write: E")

    def atrace_S(self, functionname, cookie ):
        self.m_logger.error(f"tracing_mark_write: S|{self.m_pid}|{functionname}|{cookie}")

    def atrace_F(self, functionname, cookie ):
        self.m_logger.error(f"tracing_mark_write: F|{self.m_pid}|{functionname}|{cookie}")

    def atrace_C(self, name, count ):
        self.m_logger.error(f"tracing_mark_write: C|{self.m_pid}|{name}|{count}")


"""
##################################################################
Global Object
##################################################################
"""
ftraceLog = FtraceLog()


if __name__ == "__main__":
    
    from  libPython.core.ftrace_log import ftraceLog
    import time
    import random

    ftraceLog.LogInitial(__file__)
    ftraceLog.atrace_B("SUMALL")
    sum = 0
    for i in range(10):
        ftraceLog.atrace_B("sum_one")
        
        time.sleep(1)
        ftraceLog.atrace_C("random1", int(random.random()*1000))

        ftraceLog.atrace_B("X")
        time.sleep(1)
        ftraceLog.atrace_E()

        time.sleep(1)
        ftraceLog.atrace_S("mul", i)

        ftraceLog.atrace_E()
        time.sleep(2)

        ftraceLog.atrace_F("mul", i)
        ftraceLog.atrace_C("random2", int(random.random()*1000))

    ftraceLog.atrace_E()

    print('Done')
