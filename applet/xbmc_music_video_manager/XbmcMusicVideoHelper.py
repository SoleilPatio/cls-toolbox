#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
#................................................................................
# Add libPython\.. into PYTHONPATH if in unit test
#................................................................................
import sys
import os
import codecs
import re
import textwrap

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import libPython.core.util as core
import libPython.File.FileInfo as fileinfo




__version_info__ = ('0','0','1')
__version__ = '-'.join(__version_info__)

MUSIC_VIDEO_NFO_TEMPLATE = "<musicvideo>\n\
<title>%s</title>\n\
<artist>%s</artist>\n\
<album>%s</album>\n\
<genre></genre>\n\
<director></director>\n\
<composer></composer>\n\
<studio></studio>\n\
<year></year>\n\
<runtime></runtime>\n\
</musicvideo>"



def GenerateNFO( video_file_name ):
    #...................................
    # Create *.nfo
    #...................................
    nfo_file_name = os.path.splitext(video_file_name)[0] + ".nfo"
    
    file_status = fileinfo.check_file_status(video_file_name)
    filename_no_ext = file_status.get("fn_noext","")
    # print("video_file_name=",video_file_name)
    mo = re.match(r"((\d+)\s*-)?\s*([^-]*)\s*-\s*([^-]*)(\s*-\s*\[(.*)\])?", filename_no_ext)
    if mo:
        # print("mo=",mo.groups())
        artist_name = mo.group(3).strip()
        title_name = mo.group(4).strip()
        options_str = mo.group(6)
        if options_str and "no_nfo" in options_str: #bypass filename that contains "no_nfo"
            return

    album_name = file_status.get("fn_parent_dirname","")

    
    with codecs.open(nfo_file_name, 'w' , encoding='utf-8') as outfile:
        outfile.write(MUSIC_VIDEO_NFO_TEMPLATE % (title_name,artist_name,album_name))
    
    print("Create:%s"%nfo_file_name)

    #...................................
    # Create *.tbn (*.jpg)
    # ffmpeg -i "Vivian Dvd-1-1 Messages to Japanese Fan.m4v" -ss 00:00:10.000 -vframes 1 output.jpg
    #...................................
    jpg_file_name = os.path.splitext(video_file_name)[0] + ".jpg"
    tbn_file_name = os.path.splitext(video_file_name)[0] + ".tbn"
    command = r'ffmpeg -y -i "%s" -ss 00:00:10.000 -vframes 1 "%s"' % (video_file_name, jpg_file_name)
    
    (ret_code, std_out, std_err) = core.RunCommand(command, text_mode=False) #Use UTF-8 mode
    if ret_code != 0:
        print("[ERROR]:", std_err)
    else:
        try:
            os.remove(tbn_file_name)
        except:
            pass
        os.rename(jpg_file_name, tbn_file_name)
        print("Create:%s"%tbn_file_name)

    # print("nfo=", nfo_file_name)
    # print("file_status=", core.StrObj(file_status))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        prog='XBMC Music Video Helper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            additional information:
                1. file name ends with "- [no_nfo]" will be ignored.
            '''))
    parser.add_argument("dir", help="music video directories")
    parser.add_argument("-r",  action="store_true", help="recursive process")
    
    # args = parser.parse_args([r"\\MNEMOSYNE\\NDK-Data\DB_AV_多媒體資料\\VIDEO_影片\\[MUSIC VIDEOS]"])
    args = parser.parse_args() #[NOTE]: Normal Mode

    print("args = ", args)


    #...................................
    # Find files to process
    #...................................
    file_list = []
    video_ext_list = ["mkv", "m4v", "mp4", "avi", "webm", "mpg"]
    fileinfo.list_all_files(file_list, args.dir, video_ext_list, args.r )
    print("Files=", core.StrObj(file_list))

    for f in file_list:
        GenerateNFO(f)

    


    
    
    print("Done")