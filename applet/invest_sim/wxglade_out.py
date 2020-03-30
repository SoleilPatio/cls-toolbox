#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.5 on Mon Mar 30 23:59:12 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1500, 900))
        self.GUI_statusbar = self.CreateStatusBar(3)
        self.GUI_btn_cloudload = wx.Button(self, wx.ID_ANY, u"雲端讀取")
        self.GUI_btn_inputdata = wx.Button(self, wx.ID_ANY, u"輸入資料")
        self.GUI_btn_test = wx.Button(self, wx.ID_ANY, u"測試")
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY)
        self.panel_2 = wx.Panel(self.window_1, wx.ID_ANY)
        self.matplotlib_figure = Figure()
        self.GUI_matplotlib_canvas = FigureCanvas(self.panel_2, wx.ID_ANY, self.matplotlib_figure)
        self.GUI_matplotlib_toolbar = NavigationToolbar(self.GUI_matplotlib_canvas)
        self.GUI_matplotlib_toolbar.Realize()
        self.GUI_matplotlib_toolbar.update()
        self.panel_1 = wx.Panel(self.panel_2, wx.ID_ANY)
        self.ui_initial_position = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        self.ui_extra_position = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.ui_extra_time = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.notebook_1 = wx.Notebook(self.window_1, wx.ID_ANY, style=wx.NB_BOTTOM)
        self.ui_page_message = wx.ScrolledWindow(self.notebook_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.GUI_message = wx.TextCtrl(self.ui_page_message, wx.ID_ANY, u"顯示訊息在這裏", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.ui_page_log = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.GUI_log = wx.TextCtrl(self.ui_page_log, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnCloudLoad, self.GUI_btn_cloudload)
        self.Bind(wx.EVT_BUTTON, self.OnInputData, self.GUI_btn_inputdata)
        self.Bind(wx.EVT_BUTTON, self.OnTest, self.GUI_btn_test)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("InvestSim")
        self.GUI_statusbar.SetStatusWidths([-1, -1, -5])

        # statusbar fields
        GUI_statusbar_fields = ["Ready", "", ""]
        for i in range(len(GUI_statusbar_fields)):
            self.GUI_statusbar.SetStatusText(GUI_statusbar_fields[i], i)
        self.GUI_btn_cloudload.SetBitmap(wx.Bitmap(".\\res\\cloudload-30x30.png", wx.BITMAP_TYPE_ANY))
        self.GUI_btn_inputdata.SetBitmap(wx.Bitmap(".\\res\\cloudload-30x30.png", wx.BITMAP_TYPE_ANY))
        self.GUI_btn_test.SetBitmap(wx.Bitmap(".\\res\\cloudload-30x30.png", wx.BITMAP_TYPE_ANY))
        self.ui_page_message.SetScrollRate(10, 10)
        self.window_1.SetMinimumPaneSize(100)
        self.window_1.SetSashGravity(0.5)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Input = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, u"輸入"), wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(3, 2, 0, 0)
        Sizer_Chart = wx.StaticBoxSizer(wx.StaticBox(self.panel_2, wx.ID_ANY, u"線圖"), wx.VERTICAL)
        Sizer_Function = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"功能"), wx.HORIZONTAL)
        Sizer_Function.Add(self.GUI_btn_cloudload, 0, wx.ALL, 2)
        Sizer_Function.Add(self.GUI_btn_inputdata, 0, wx.ALL, 2)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add((0, 0), 0, 0, 0)
        Sizer_Function.Add(self.GUI_btn_test, 0, wx.ALL, 2)
        sizer_1.Add(Sizer_Function, 0, wx.ALL | wx.EXPAND, 2)
        Sizer_Chart.Add(self.GUI_matplotlib_canvas, 1, wx.ALL | wx.EXPAND, 2)
        Sizer_Chart.Add(self.GUI_matplotlib_toolbar, 0, wx.EXPAND, 0)
        sizer_2.Add(Sizer_Chart, 1, wx.ALL | wx.EXPAND, 0)
        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, u"初始口數")
        grid_sizer_1.Add(label_1, 0, wx.ALL, 2)
        grid_sizer_1.Add(self.ui_initial_position, 0, wx.ALL, 2)
        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, u"加碼口數")
        grid_sizer_1.Add(label_2, 0, wx.ALL, 2)
        grid_sizer_1.Add(self.ui_extra_position, 0, wx.ALL, 2)
        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, u"加碼次數")
        grid_sizer_1.Add(label_3, 0, wx.ALL, 2)
        grid_sizer_1.Add(self.ui_extra_time, 0, wx.ALL, 2)
        Sizer_Input.Add(grid_sizer_1, 1, 0, 0)
        self.panel_1.SetSizer(Sizer_Input)
        sizer_2.Add(self.panel_1, 0, 0, 0)
        self.panel_2.SetSizer(sizer_2)
        sizer_3.Add(self.GUI_message, 1, wx.ALL | wx.EXPAND, 2)
        self.ui_page_message.SetSizer(sizer_3)
        sizer_4.Add(self.GUI_log, 1, wx.ALL | wx.EXPAND, 2)
        self.ui_page_log.SetSizer(sizer_4)
        self.notebook_1.AddPage(self.ui_page_message, u"訊息")
        self.notebook_1.AddPage(self.ui_page_log, "log")
        self.window_1.SplitHorizontally(self.panel_2, self.notebook_1, 450)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnCloudLoad(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'OnCloudLoad' not implemented!")
        event.Skip()

    def OnInputData(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'OnInputData' not implemented!")
        event.Skip()

    def OnTest(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'OnTest' not implemented!")
        event.Skip()

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
