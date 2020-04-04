# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import logging
import matplotlib.pyplot as plt
from libinvestsim.investsim_control import InvestSimControl
from libinvestsim.ivs_view_quicksim import IvsViewQuickSim

from wxglade_out import *


"""
========================================================
[Global Config]
========================================================
"""
EXE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(EXE_DIR, "config.json")
logging.basicConfig(level=logging.DEBUG)

CACHE_DIR = os.path.join( EXE_DIR, "cache" )
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)



"""
========================================================
Logging Handler
========================================================
"""
class LoggingHandler(logging.StreamHandler):
    def SetGuiObjectToLog(self, gui_log_obj):
        self.gui_log_obj = gui_log_obj

    def SetGuiStatusbar(self, gui_statusbar_obj):
        self.gui_statusbar_obj = gui_statusbar_obj

    def emit(self, record):

        msg_formatted = self.format(record)
        if( self.gui_log_obj ):
            self.gui_log_obj.AppendText( "%s:%s:%s\n" % (record.levelname, record.module, msg_formatted) )

        if( self.gui_statusbar_obj ):
            self.gui_statusbar_obj.SetStatusText(msg_formatted, i=2)

        # print("format_msg=", self.format(record))
        # print("message=", record.message)
        # print("module=", record.module)
        # print("filename=", record.filename)
        # print("funcName=", record.funcName)
        # print("lineno=", record.lineno)
        # print("levelname=", record.levelname)
        # print("name=", record.name)
        # print("pathname=", record.pathname)
        # print("processName=", record.processName)
        # print("process=", record.process)
        # print("threadName=", record.threadName)
        # print("thread=", record.thread)

# end of LoggingHandler


def mpl_Plot(axes, y_values, line_style='.-'):
    print("y_values=",y_values)
    axes.plot(y_values,line_style)




"""
========================================================
InvestSimFrame Windows
========================================================
"""
class InvestSimFrame(MyFrame):
    def __init__(self, *args, **kwds):
        super(InvestSimFrame, self).__init__(*args, **kwds)
        #Control
        self.Control = InvestSimControl()
        #View: QuickSim
        self.ViewQuickSim = IvsViewQuickSim( cachedir=CACHE_DIR)
        self.ViewQuickSim.RestoreGuiFromCache(self)
        #My event handler
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    
    def OnCloudLoad(self, event):  # wxGlade: MyFrame.<event_handler>
        self.GUI_statusbar.SetStatusText(r"讀取雲端資料中...", i=0)
        self.Control.Initial(CONFIG_FILE)
        self.Control.LoadData()
        self.Control.Policy()
        self.GUI_statusbar.SetStatusText(r"雲端資料讀取完畢!", i=0)


    def OnInputData(self, event):  # wxGlade: MyFrame.<event_handler>
        import webbrowser
        self.GUI_statusbar.SetStatusText(r"開啓Google試算表輸入資料", i=0)
        webbrowser.open('https://docs.google.com/spreadsheets/d/1i0Mr9BCpGDVyScA808_nTz70nM-oSo-T7gmBSxqFL-E/')
        webbrowser.open('https://docs.google.com/spreadsheets/d/1qJ0eT6sjo_f8dguSk7ccsd11v1o1BbR73LJUslur1W0/')
        webbrowser.open('https://docs.google.com/spreadsheets/d/1WfF20vvAjZqSrwiN1CAzxXGm6X_RGjjdduF0Kukv-o8/')


    def OnQuickApply(self, event):  # wxGlade: MyFrame.<event_handler>
        self.ViewQuickSim.Render(   
            self,                           #Frame object
            self.matplotlib_figure_2,       #Figure (Canvas of matplotlib)
            self.GUI_matplotlib_canvas_2    #Canvas
            )



    def OnClose(self, event):  # wxGlade: MyFrame.<event_handler>
        # import pickle 
        # file = open('important', 'wb')
        # pickle.dump(self.__dict__, file)
        # file.close()
        print("[CLS]: Windows Close!")
        self.Destroy()



    def OnTest(self, event):  # wxGlade: MyFrame.<event_handler>
        count=1
        #[CLS] matplot test
        figure = self.matplotlib_figure

        figure.clf()
        axes_1 = figure.add_subplot(count+1,(count+2)%3+1,1)

        count = (count+1)%4

        if count == 0:
            mpl_Plot(axes_1, self.Control.data["XINA50"][u"回合最大淨值"],"-")
            logging.debug(u"回合最大淨值")
        elif count == 1:
            mpl_Plot(axes_1, self.Control.data["XINA50"][u"當日淨值"],".-")
            logging.debug(u"當日淨值")
        elif count == 2:
            mpl_Plot(axes_1, self.Control.data["XINA50"][u"當日停損淨值"],"x-")
            logging.debug(u"當日停損淨值")
        else:
            axes_1.cla()
            logging.debug(u"clear")

        self.GUI_matplotlib_canvas.draw() #[CLS] force update canvas







# end of class MainFrame


"""
========================================================
InvestSim Application
========================================================
"""
class InvestSimApp(wx.App):
    def OnInit(self):
        self.frame = InvestSimFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


"""
========================================================
Main Entry
========================================================
"""

if __name__ == "__main__":
    app = InvestSimApp(0)

    #[CLS]: Config GUI log/message object
    gui_log_handler = LoggingHandler()
    gui_log_handler.SetGuiObjectToLog(app.frame.GUI_log)
    gui_log_handler.SetGuiStatusbar(app.frame.GUI_statusbar)
    logging.getLogger().addHandler(gui_log_handler)


    #Enter App main loop
    app.MainLoop()


    print("\nDone")
