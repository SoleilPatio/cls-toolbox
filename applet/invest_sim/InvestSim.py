# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import logging
import matplotlib.pyplot as plt
from libinvestsim.investsim_control import InvestSimControl
import libinvestsim.ivs_policy as policy 
from wxglade_out import *


#[Global Config]
EXE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(EXE_DIR, "config.json")
logging.basicConfig(level=logging.DEBUG)

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




#test
count = 0

class InvestSimFrame(MyFrame):
    def __init__(self, *args, **kwds):
        super(InvestSimFrame, self).__init__(*args, **kwds)
        #InvestSimControl
        self.Control = InvestSimControl()

    
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

        #--------------------------------------------------------
        #1. Get data from GUI
        #--------------------------------------------------------
        GUI_Data = {}
        GUI_Data[u"產品"]=self.GUI_quick_product_sel.GetStringSelection()
        GUI_Data[u"乘數"]=float(self.GUI_quick_multiplier.GetStringSelection())
        GUI_Data[u"最大淨值"]=self.GUI_quick_max_netvalue.GetValue()*1000 #return float
        GUI_Data[u"目前淨值"]=self.GUI_quick_current_netvalue.GetValue()*1000 #return float
        GUI_Data[u"可損失比率"]=self.GUI_quick_stoploss_rate.GetValue() #return float
        GUI_Data[u"目前價格"]=self.GUI_quick_current_price.GetValue() #return float

        GUI_Data["TRIAL"]=[]

        #Trial 1 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=self.GUI_Q_T1_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=self.GUI_Q_T1_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=self.GUI_Q_T1_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=self.GUI_Q_T1_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 2 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=self.GUI_Q_T2_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=self.GUI_Q_T2_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=self.GUI_Q_T2_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=self.GUI_Q_T2_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 3 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=self.GUI_Q_T3_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=self.GUI_Q_T3_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=self.GUI_Q_T3_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=self.GUI_Q_T3_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 4 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=self.GUI_Q_T4_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=self.GUI_Q_T4_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=self.GUI_Q_T4_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=self.GUI_Q_T4_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        print("GUI_Data=",str(GUI_Data).decode('unicode-escape'))

        
        #--------------------------------------------------------
        #2. Calculate
        #--------------------------------------------------------
        Stop_Data = []
        for i in range(len(GUI_Data[u"TRIAL"])):
            stop_data = policy.CalcStopPrice(  GUI_Data[u"最大淨值"], GUI_Data[u"目前淨值"], GUI_Data[u"可損失比率"], 
                        GUI_Data[u"乘數"], 
                        GUI_Data[u"目前價格"], GUI_Data[u"TRIAL"][i][u"加碼價格"],
                        GUI_Data[u"TRIAL"][i][u"目前口數"], GUI_Data["TRIAL"][i][u"加碼口數"], GUI_Data[u"TRIAL"][i][u"分批次數"] )
            Stop_Data.append(stop_data)

        print("Stop_Data=",str(Stop_Data).decode('unicode-escape'))
            

        #--------------------------------------------------------
        #3. Plot
        #--------------------------------------------------------
        figure = self.matplotlib_figure_2
        figure.clf()
        axes = figure.add_subplot(1,1,1)

        for i, stop_data in enumerate(Stop_Data):
            if stop_data:
                axes.eventplot(stop_data[u"各次加碼價格"],orientation='vertical',lineoffsets=i+1,linelengths=0.2,
                                colors='C{}'.format(i))


        self.GUI_matplotlib_canvas_2.draw() #[CLS] force update canvas





    def OnTest(self, event):  # wxGlade: MyFrame.<event_handler>
        global count
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

class InvestSimApp(wx.App):
    def OnInit(self):
        self.frame = InvestSimFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp



if __name__ == "__main__":
    app = InvestSimApp(0)

    #[CLS]: Config GUI log/message object
    gui_log_handler = LoggingHandler()
    gui_log_handler.SetGuiObjectToLog(app.frame.GUI_log)
    gui_log_handler.SetGuiStatusbar(app.frame.GUI_statusbar)
    logging.getLogger().addHandler(gui_log_handler)

    # #[CLS] matplot test
    # figure = app.frame.matplotlib_figure
   
    # axes = figure.add_subplot(311)
    # import numpy as np
    # t = np.arange(0.0, 3.0, 0.1)
    # s = np.sin(2 * np.pi * t)
    # axes.plot(t,s,'.-')
    # app.frame.GUI_matplotlib_canvas.draw()

    # axes = figure.add_subplot(312)
    # import numpy as np
    # t = np.arange(0.0, 30.0, 0.01)
    # s = np.sin(2 * np.pi * t)
    # axes.plot(t,s)
    # app.frame.GUI_matplotlib_canvas.draw()

    # axes = figure.add_subplot(313)
    # import numpy as np
    # t = np.arange(0.0, 300.0, 0.01)
    # s = np.sin(2 * np.pi * t)
    # axes.plot(t,s)
    # app.frame.GUI_matplotlib_canvas.draw()


    #Enter App main loop
    app.MainLoop()



    print("\nDone")
