
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

    def cache_file_product(self, productname):
        return os.path.join(self.cache_dir, "cache_view_quicksim-%s.json"%productname)



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
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T1_avg_buy_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T1_avg_buy_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T1_avg_buy_count, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 2 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][1]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T2_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T2_avg_buy_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T2_avg_buy_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T2_avg_buy_count, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 3 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][2]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T3_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T3_avg_buy_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T3_avg_buy_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T3_avg_buy_count, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 4 ------------------------
        if direction == 'from': #Read operation
            Trial_Data={}
        else:
            Trial_Data = GUI_Data["TRIAL"][3]

        util.WxWidgetDataSync( Trial_Data, u"目前口數", Frame.GUI_Q_T4_current_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼價格", Frame.GUI_Q_T4_avg_buy_price, direction )
        util.WxWidgetDataSync( Trial_Data, u"加碼口數", Frame.GUI_Q_T4_avg_buy_pos, direction )
        util.WxWidgetDataSync( Trial_Data, u"分批次數", Frame.GUI_Q_T4_avg_buy_count, direction )

        if direction == 'from': #Read operation
            GUI_Data["TRIAL"].append(Trial_Data)

        #End of Trial ------------------------



    def RestoreGuiFromCache(self, Frame):
        self.RestoreGuiFromCacheFromJson(Frame, self.cache_file)

    def RestoreGuiFromCacheByProduct(self, Frame, productname):
        self.RestoreGuiFromCacheFromJson(Frame, self.cache_file_product(productname))

    def RestoreGuiFromCacheFromJson(self, Frame, json_file):
        if not os.path.isfile(json_file):
            logging.warn("no cached file found:%s"%json_file)
            return
        #Load cached setting from file
        GUI_Data=util.LoadObjFromJson(json_file)
        #Restore setting to GUI
        self.GuiDataSync(GUI_Data, Frame, direction='to')

    """
    --------------------------------------------------------
    Read GUI input data to GUI_Data object and return
    --------------------------------------------------------
    """
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
        M_LINELENGTH = 0.2

        Figure.clf()
        axes = Figure.add_subplot(1,1,1)
        axes.grid(axis='y', alpha=0.8, linewidth=0.5, linestyle=':')

        #Current Price
        axes.axhline(GUI_Data[u"目前價格"], ls='-', color='C8', alpha=0.1, lw=5, zorder = 0) #current price


        #For each Trial
        for i, stop_data in enumerate(Stop_Data):
            if stop_data:
                avg_buy_price_list = stop_data[u"各次加碼價格"]
                avg_buy_pos_list = stop_data[u"各次加碼口數"]
                avg_buy_pos_ttl_list = stop_data[u"各次加碼總口數"]
                sign = stop_data[u"多空"]

                color = 'C{}'.format(i)
                X = i+1 #X-axis value
                axes.eventplot( avg_buy_price_list, 
                                orientation='vertical', lineoffsets=X, linelengths=M_LINELENGTH, 
                                linewidths=0.8,
                                colors=color) #colors='C0','C1','C2',....,'C9'
                if sign > 0:
                    axes.plot(X, avg_buy_price_list[0],  'v', color=color) #Start avg_buy
                else:
                    axes.plot(X, avg_buy_price_list[0],  '^', color=color) #Start avg_buy
                
                axes.plot(X, avg_buy_price_list[-1], 'x', color=color) #STOP point

                #text: price
                for i, y_price in enumerate(avg_buy_price_list):
                    change = y_price-GUI_Data[u"目前價格"]
                    change_p = format((change/GUI_Data[u"目前價格"])*100,".1f")
                    text_price="%s(%s%%/%d)"%( format(y_price,".1f"), change_p, change )
                    axes.text(X + M_LINELENGTH/2, y_price, text_price, color=color)
                    
                    #text: position info
                    if i != len(avg_buy_price_list)-1:
                        text_pos = "%+d(%d)"%(avg_buy_pos_list[i],avg_buy_pos_ttl_list[i]) 
                        axes.text(X - M_LINELENGTH/2, y_price, text_pos, color=color, horizontalalignment="right")
                    else:
                        text_pos = u"(STOP)"
                        axes.text(X - M_LINELENGTH/2, y_price, text_pos, color=color, horizontalalignment="right", 
                                    bbox=dict(facecolor=color, alpha=0.2) )
                    
                



        Canvas.draw() #[CLS] force update canvas


        #--------------------------------------------------------
        #4. Save to Cache
        #--------------------------------------------------------
        if self.cache_file:
            util.SaveObjToJson(GUI_Data, self.cache_file)
            util.SaveObjToJson(GUI_Data, self.cache_file_product(GUI_Data[u"產品"]))


