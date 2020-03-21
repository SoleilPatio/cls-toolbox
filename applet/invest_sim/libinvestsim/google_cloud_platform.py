# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

# [CLS]: 假如有問題,執行: pip install --upgrade google-api-python-client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleCloudPlatform(object):
    def __init__(self, client_secret_file):
        super(GoogleCloudPlatform, self).__init__()

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        # [CLS] scopes 可以是多個scope字串(給list?)
        self.scopes = [
            # [CLS] 設定 我們的 App 會讀取 user 的 google spreadsheet
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/userinfo.email'
        ]

        self.app_name = 'ClsGoogleService'

        # [CLS]: google sample default arguments:
        #       flags = (auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=False)
        self.flags = self._get_flags()
        self.client_secret_file = client_secret_file

        # [CLS]: open browser get credential and store in C:\Users\cloud\.credentials
        self.credentials = self.GetCredentials()

        # [CLS]: 根據認證產生認證的http，以後據此操作 (httplib2再包一層?)
        self.http = self.credentials.authorize(httplib2.Http())


    def _get_flags(self):
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()  # [CLS]: 加了四個參數
        except ImportError:
            flags = None
        return flags

    def GetCredentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        # [CLS]: 會在home下建立.credentials目錄,以及認證cache jason file
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        # [CLS]: 認證快取存在這裏 C:\Users\cloud\.credentials
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.client_secret_file, self.scopes)
            flow.user_agent = self.app_name
            if flags:
                credentials = tools.run_flow(
                    flow, store, self.flags)    # [CLS]: 打開網頁跑取得認證的flow
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    def GetGoogleSheetsApiService(self):
        service = GoogleSheetsApiService()
        service.CreateService( self.http)
        return service



class GoogleSheetsApiService(object):
    def __init__(self):
        super(GoogleSheetsApiService, self).__init__()
        self.service = None
        self.spread_sheet_id = None  #ex: '1i0Mr9BCpGDVyScA808_nTz70nM'

    def CreateService(self, http):
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)
        return self.service


    """
    spreadsheet_Id sample: '1i0Mr9BCpGDVyScA808_nTz70nM'
    """
    def OpenSpreadSheet(self, spreadsheet_id):
        self.spread_sheet_id = spreadsheet_id


    """
    range_name sample:
        'XINA50' worksheet name
        'Class Data!A2:E' with range
    """
    def GetSheetValues(self, range_name ):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spread_sheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values




if __name__ == '__main__':
    # CLIENT_SECRET_FILE = 'client_secret.json'
    # CLIENT_SECRET_FILE = ur"C:\\APN\\USERS\\clouds\\Google 雲端硬碟\\MyPrivy\\憑證\\Google-API\\hello-world-google-api\\client_id(hello-world-google-api-client).json"
    CLIENT_SECRET_FILE = ur"C:\\APN\\USERS\\clouds\\Google 雲端硬碟\\MyPrivy\\憑證\\Google-API\\invest-sim-google-api\\client_secret_invest-sim.json"

    # main()
    # 指定 sheet ID, 你可以從 URL 得到 ID.
    spreadsheetId = '1i0Mr9BCpGDVyScA808_nTz70nM-oSo-T7gmBSxqFL-E'

    google_service = GoogleCloudPlatform(CLIENT_SECRET_FILE)
    sheets_srv = google_service.GetGoogleSheetsApiService()
    sheets_srv.OpenSpreadSheet(spreadsheetId)

    print("XINA50=", sheets_srv.GetSheetValues( 'XINA50'))
    print("2454=", sheets_srv.GetSheetValues( '2454'))

