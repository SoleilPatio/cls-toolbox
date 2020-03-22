# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import matplotlib.pyplot as plt


from libinvestsim.ivs_config import IvsConfig
from libinvestsim.libcommon.google_cloud_platform import GoogleCloudPlatform


EXE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(EXE_DIR, "config.json")


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

    """
    Load Config
    """
    ivs_conf = IvsConfig()
    # ivs_conf.SaveDefaultConfig()
    data = ivs_conf.LoadConfig(CONFIG_FILE)
    ivs_conf.Show()
    
    """
    Connect Google API
    """
    gcp = GoogleCloudPlatform(ivs_conf.secret_file())
    sheets_api = gcp.GetGoogleSheetsApiService()

    """
    Load Data
    """
    sheets_api.OpenSpreadSheet(ivs_conf.spreadsheet_id_investsim_daily_track())


    print("XINA50=", sheets_api.GetSheetValues('XINA50'))
    print("2454=", sheets_api.GetSheetValues('2454'))



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
    # print("\nDonw")
