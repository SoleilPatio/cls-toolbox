#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
#------------------------------------------------------------------------------
if __name__ == "__main__": import _libpythonpath_ # Add libPython\.. into PYTHONPATH when unittest
#------------------------------------------------------------------------------
import libPython.core.util as util
import libPython.core.util_ex as util_ex

import argparse
import requests
from pathlib import Path

def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {
        'message': msg,
        'stickerPackageId': 11539,
        'stickerId':52114146
    }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

TOKEN_FILE = {
    "Clouds 機器人": r"C:\Users\cloud\GoogleDrive\MyPrivy\憑證\LINE\clouds_to_Clouds 機器人.token.txt",
    "YunTin.com": r"C:\Users\cloud\GoogleDrive\MyPrivy\憑證\LINE\clouds_to_YunTin.com.token.txt",
}

TOKEN_FILE_2 = {
    "Clouds 機器人": r"C:\APN\U\USERDATA\MyPrivy\LINE\clouds_to_Clouds 機器人.token.txt",
    "YunTin.com": r"C:\APN\U\USERDATA\MyPrivy\LINE\clouds_to_YunTin.com.token.txt",
}


if __name__ == "__main__":
    parser  = argparse.ArgumentParser(description='Send notification message through line.')
    parser.add_argument('-w', '--who', type=str, default='Clouds 機器人')
    parser.add_argument('message', type=str)
    args = parser.parse_args()

    try:
        token = Path(TOKEN_FILE[args.who]).read_text()
    except:
        token = Path(TOKEN_FILE_2[args.who]).read_text()

    ret = lineNotifyMessage(token, args.message)
    print(f"line notify ret = {ret}")
    
