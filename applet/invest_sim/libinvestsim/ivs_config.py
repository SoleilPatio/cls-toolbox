# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from libcommon.json_config import JsonConfig


class IvsConfig(object):
    def __init__(self):
        super(IvsConfig, self).__init__()
        self.file_path = None
        self.data = {}  # json content

    def SaveDefaultConfig(self, file_path):
        self.file_path = file_path
        self.data = {}
        data = self.data

        data["google_client_secret_file"] = r'C:\APN\USERS\clouds\Google 雲端硬碟\MyPrivy\憑證\Google-API\invest-sim-google-api\client_secret_invest-sim.json'
        data["ssid_investsim_daily_track"] = '1i0Mr9BCpGDVyScA808_nTz70nM-oSo-T7gmBSxqFL-E'

        JsonConfig().SaveData(data, self.file_path)
        print("[INFO]: config file saved: %s" % self.file_path)

    def LoadConfig(self, file_path):
        self.file_path = file_path
        self.data = JsonConfig().Load(self.file_path)
        print("[INFO]: config file loaded: %s" % self.file_path)
        return self.data

    def Show(self):
        JsonConfig().ShowData(self.data)
        self.SanityCheck()

    def SanityCheck(self):
        data = self.data
        print("file check: %s is %s" % ( data["google_client_secret_file"], os.path.exists(data["google_client_secret_file"]) ))


    def secret_file(self):
        return self.data["google_client_secret_file"]

    def spreadsheet_id_investsim_daily_track(self):
        return self.data["ssid_investsim_daily_track"]




if __name__ == '__main__':
    CONF_FILE="test-config-ivs.json"

    ivs_conf=IvsConfig()

    ivs_conf.SaveDefaultConfig(CONF_FILE)
    ivs_conf.LoadConfig(CONF_FILE)
    ivs_conf.Show()
