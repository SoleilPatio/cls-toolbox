# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json
import matplotlib.pyplot as plt


from libinvestsim.ivs_config import IvsConfig
from libinvestsim.libcommon.google_cloud_platform import *


EXE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(EXE_DIR, "config.json")


class InvestSimApp(object):
    def __init__(self):
        super(InvestSimApp, self).__init__()
        self.config = IvsConfig()  # IvsConfig Object
        self.gcp = None  # GoogleCloudPlatform object
        self.sheet_api = None  # GoogleSheetsApiService()
        self.data = {}  #whole data


    def Initial(self, config_file_name):
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
        self.load_data_daily_track()
        self.load_data_data()
        self.load_data_dry_run()

    def load_data_daily_track(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_daily_track())

        for sheet_name in self.sheets_api.GetSheetNames():
            values = self.sheets_api.GetSheetValues(sheet_name)
            print(sheet_name,"=", values )
            col_data = SheetRowDataToColumnData(values)
            self.data[sheet_name] = col_data    #sheet_name is product name,use as index
        
        print("self.data =", json.dumps(self.data, indent=4))
        # print("XINA50=", self.sheets_api.GetSheetValues('XINA50'))
        # print("2454=", self.sheets_api.GetSheetValues('2454'))


    def load_data_data(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_data())

    def load_data_dry_run(self):
        self.sheets_api.OpenSpreadSheet(
            self.config.spreadsheet_id_investsim_run())



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
