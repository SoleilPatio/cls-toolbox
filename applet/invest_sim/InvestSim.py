# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json
import matplotlib.pyplot as plt


from libinvestsim.ivs_config import IvsConfig
from libinvestsim.ivs_policy import IvsPolicy
from libinvestsim.libcommon.google_cloud_platform import *
from libinvestsim.libcommon.json_config import JsonConfig


EXE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(EXE_DIR, "config.json")


class InvestSimApp(object):
    def __init__(self):
        super(InvestSimApp, self).__init__()
        self.config = IvsConfig()  # IvsConfig Object
        self.gcp = None  # GoogleCloudPlatform object
        self.sheet_api = None  # GoogleSheetsApiService()
        self.data = {}  # whole data
        self.data_dir = ""  #temp data directory

    def Initial(self, config_file_name):
        """
        temp data directory
        """
        self.data_dir = os.path.join( os.path.dirname(config_file_name), "data" )
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        """
        Load Config
        """
        # self.config.SaveDefaultConfig()
        self.config.LoadConfig(config_file_name)
        self.config.Show()

        """
        Connect Google API
        """
        self.gcp = GoogleCloudPlatform(self.config.secret_file())
        self.sheets_api = self.gcp.GetGoogleSheetsApiService()

    def LoadData(self):
        self.loaddata_daily_track()
        self.loaddata_data()
        self.loaddata_dry_run()

    def loaddata_daily_track(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_daily_track())

        for sheet_name in self.sheets_api.GetSheetNames():
            values = self.sheets_api.GetSheetValues(sheet_name)
            print("[INFO]: loading %s daily track ..."%sheet_name)
            col_data = SheetRowDataToColumnData(values)
            # sheet_name is product name,use as index
            self.data[sheet_name] = col_data

    def loaddata_data(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_data())

        sheet_name_list = self.sheets_api.GetSheetNames()
        values = self.sheets_api.GetSheetValues( sheet_name_list[0])  # Use the 1st sheet to load product spec
        dic_objs = SheetRowDataToDicObj(values)
        for key in dic_objs:
            if key in self.data:
                self.data[key].update(dic_objs[key])
            else:
                self.data[key] = dic_objs[key]

    def loaddata_dry_run(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_run())


    def Policy(self):
        for key in self.data:
            print("[INFO]: calculate %s ..."%key)
            out_dict = IvsPolicy().CalProduct(self.data[key] )
            
            out_json_filename = os.path.join( self.data_dir , "%s_out.json"%key )
            print("[INFO]: save calculated output to %s ..." % out_json_filename )
            JsonConfig().SaveData(out_dict, out_json_filename  )

            lat_json_filename = os.path.join( self.data_dir , "%s_late.json"%key )
            lat_dict = IvsPolicy().UtilKeepOnlyLatestRecord(out_dict)
            print("[INFO]: save only latest output to %s ..." % lat_json_filename )
            JsonConfig().SaveData(lat_dict, lat_json_filename  )

            all_json_filename = os.path.join( self.data_dir , "%s_all.json"%key )
            print("[INFO]: save all data to %s ..." % all_json_filename )
            JsonConfig().SaveData(self.data[key], all_json_filename  )




class StockPrice(object):
    def __init__(self):
        self.start = 9800  # 股價開始
        self.end = 7800  # 股價結束

    def GetValues(self):
        values = []
        for price in range(self.start, self.end, 1 if self.end > self.start else -1):
            values.append(price)
        return values


class FuturePosition(object):
    def __init__(self):
        pass

    def ApplyPolicy(self, StockPrice):
        add_range = StockPrice.start * 0.05  # 5% 加碼
        positions = []
        counter = 0
        position = 0
        for price in range(StockPrice.start, StockPrice.end, 1 if StockPrice.end > StockPrice.start else -1):
            counter += 1
            if counter % add_range == 0:
                position += 1
            positions.append(position)

        return positions


def OpenBroswer():
    import webbrowser
    webbrowser.open(
        'https://docs.google.com/spreadsheets/d/1i0Mr9BCpGDVyScA808_nTz70nM-oSo-T7gmBSxqFL-E/')


if __name__ == '__main__':

    MainApp = InvestSimApp()

    MainApp.Initial(CONFIG_FILE)
    MainApp.LoadData()
    MainApp.Policy()

    """
    Test: clear credential
    """
    # gcp.ClearCredentials()

    # stockprice = StockPrice()
    # futureposition = FuturePosition()

    # positions = futureposition.ApplyPolicy(stockprice)

    # print(positions)

    # # plt.plot(stockprice.GetValues(), ".")
    # plt.plot(positions, "-")
    # plt.show()
    print("\nDone")
