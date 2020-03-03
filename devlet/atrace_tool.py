#!/usr/bin/env python
import sys
import os

sys.path.append(r'D:\Project\libpython')
sys.path.append(r'N:\project\libpython')
sys.path.append(r'/proj/mtk02679/project/libpython')
import Utils.CLI as cli



def cmd_TurnOnAllAtraceTag():
    print "[Narrate]: Turn on all atrace flag\n\n\n"
    
    out = cli.Run(["adb","shell", "getprop debug.atrace.tags.enableflags"])
    print "enableflags=%s"%out
    
    cli.Run("adb shell setprop debug.atrace.tags.enableflags 0xFFFFFFFF")
    cli.Run("adb shell atrace --poke_services")
    
    out = cli.Run(["adb","shell", "getprop debug.atrace.tags.enableflags"])
    print "enableflags=%s"%out
    
    

 

#------------------------------------------------------------------------------ 


def main(argv=None):
    cmd_TurnOnAllAtraceTag()



if __name__ == "__main__":
    sys.exit(main())