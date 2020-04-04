
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import logging
import ivs_policy as policy 
import libcommon.utilities as util



"""
========================================================
class IvsViewQuickSim
========================================================
"""
class IvsViewQuickSim(object):
    def __init__(self, cachedir=None):
        self.cache_dir = cachedir
        if self.cache_dir:
            self.cache_file = os.path.join(self.cache_dir, "cache_view_quicksim.json")



    def GuiDataSync(self, GUI_Data, Frame, direction):

        if direction == 'from': #Read operation
            GUI_Data.clear()

        if direction == 'to': #Read operation
            GUI_Data[u"最大淨值"] = GUI_Data[u"最大淨值"]/1000
            GUI_Data[u"目前淨值"] = GUI_Data[u"目前淨值"]/1000

        util.WxWidgetDataSync( GUI_Data, u"產品", Frame.GUI_quick_product_sel, direction )
        util.WxWidgetDataSync( GUI_Data, u"乘數", Frame.GUI_quick_multiplier, direction )             #TODO:]=float(WxGetWidgetValue(Frame.GUI_quick_multiplier))
        util.WxWidgetDataSync( GUI_Data, u"最大淨值", Frame.GUI_quick_max_netvalue, direction )      #TODO:*1000 #return float
        util.WxWidgetDataSync( GUI_Data, u"目前淨值", Frame.GUI_quick_current_netvalue, direction )  #TODO:*1000 #return float
        util.WxWidgetDataSync( GUI_Data, u"可損失比率", Frame.GUI_quick_stoploss_rate, direction ) #return float
        util.WxWidgetDataSync( GUI_Data, u"目前價格", Frame.GUI_quick_current_price, direction ) #return float

        if direction == 'from': #Read operation
            GUI_Data[u"乘數"] = int(GUI_Data[u"乘數"])
            GUI_Data[u"最大淨值"] = GUI_Data[u"最大淨值"]*1000
            GUI_Data[u"目前淨值"] = GUI_Data[u"目前淨值"]*1000


        #Trial data ------------------------
        if direction == 'from': #Read operation
            GUI_Data["TRIAL"]=[]

        #Trial 1 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][0]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T1_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T1_overweight_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T1_overweight_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T1_overweight_batches_num, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 2 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][1]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T2_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T2_overweight_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T2_overweight_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T2_overweight_batches_num, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 3 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][2]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T3_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T3_overweight_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T3_overweight_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T3_overweight_batches_num, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 4 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][3]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T4_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T4_overweight_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T4_overweight_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T4_overweight_batches_num, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #End of Trial ------------------------



    def RestoreGuiFromCache(self, Frame):
        if not os.path.isfile(self.cache_file):
            return
        #Load cached setting from file
        GUI_Data=util.LoadObjFromJson(self.cache_file)
        #Restore setting to GUI
        self.GuiDataSync(GUI_Data, Frame, direction='to')



    def LoadGuiData(self, Frame):
        #Read data from GUI
        GUI_Data = {}
        self.GuiDataSync(GUI_Data, Frame, direction='from')
        return GUI_Data



    def Render(self, Frame, Figure, Canvas ):

        #--------------------------------------------------------
        #1. Get data from GUI
        #--------------------------------------------------------
        GUI_Data = self.LoadGuiData(Frame)
        print("GUI_Data=",util.StrObj(GUI_Data))

        
        #--------------------------------------------------------
        #2. Calculate
        #--------------------------------------------------------
        Stop_Data = []
        for i in range(len(GUI_Data[u"TRIAL"])):
            #Calculate STOP price for one trial
            stop_data = policy.CalcStopPrice(  GUI_Data[u"最大淨值"], GUI_Data[u"目前淨值"], GUI_Data[u"可損失比率"], 
                        GUI_Data[u"乘數"], 
                        GUI_Data[u"目前價格"], GUI_Data[u"TRIAL"][i][u"加碼價格"],
                        GUI_Data[u"TRIAL"][i][u"目前口數"], GUI_Data["TRIAL"][i][u"加碼口數"], GUI_Data[u"TRIAL"][i][u"分批次數"] )
            Stop_Data.append(stop_data)
            logging.info("TRIAL %d: STOP DATA = \n%s"%(i, util.StrObj(stop_data)))
        


        #--------------------------------------------------------
        #3. Plot
        #--------------------------------------------------------
        Figure.clf()
        axes = Figure.add_subplot(1,1,1)

        M_LINELENGTH = 0.2

        for i, stop_data in enumerate(Stop_Data):
            if stop_data:
                data_list = stop_data[u"各次加碼價格"]
                color = 'C{}'.format(i)
                X = i+1
                axes.eventplot( data_list, 
                                orientation='vertical', lineoffsets=X, linelengths=M_LINELENGTH, 
                                linewidths=0.3,
                                colors=color) #colors='C0','C1','C2',....,'C9'
                axes.plot(X, data_list[0],  'o', color=color) #Start overweight
                axes.plot(X, data_list[-1], 'x', color=color) #STOP point

                #text: point
                for i, data in enumerate(data_list):
                    text_price=format(data,".1f")
                    if i == len(data_list)-1:
                        text_price += u"(STOP)"
                    axes.text(X + M_LINELENGTH/2, data, text_price, color=color)
                    axes.text(X - M_LINELENGTH/2, data, "+2", color=color, horizontalalignment="right")


        Canvas.draw() #[CLS] force update canvas


        #--------------------------------------------------------
        #4. Save to Cache
        #--------------------------------------------------------
        if self.cache_file:
            util.SaveObjToJson(GUI_Data, self.cache_file)


