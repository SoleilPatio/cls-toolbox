
# -*- coding: utf-8 -*-
from __future__ import print_function

import libinvestsim.ivs_policy as policy 

"""
========================================================
class IvsViewQuickSim
========================================================
"""
class IvsViewQuickSim(object):
    def __init__(self):
        pass

    def Render(self, Frame, Figure, Canvas ):

        #--------------------------------------------------------
        #1. Get data from GUI
        #--------------------------------------------------------
        GUI_Data = {}
        GUI_Data[u"產品"]=Frame.GUI_quick_product_sel.GetStringSelection()
        GUI_Data[u"乘數"]=float(Frame.GUI_quick_multiplier.GetStringSelection())
        GUI_Data[u"最大淨值"]=Frame.GUI_quick_max_netvalue.GetValue()*1000 #return float
        GUI_Data[u"目前淨值"]=Frame.GUI_quick_current_netvalue.GetValue()*1000 #return float
        GUI_Data[u"可損失比率"]=Frame.GUI_quick_stoploss_rate.GetValue() #return float
        GUI_Data[u"目前價格"]=Frame.GUI_quick_current_price.GetValue() #return float

        GUI_Data["TRIAL"]=[]

        #Trial 1 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=Frame.GUI_Q_T1_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=Frame.GUI_Q_T1_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=Frame.GUI_Q_T1_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=Frame.GUI_Q_T1_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 2 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=Frame.GUI_Q_T2_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=Frame.GUI_Q_T2_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=Frame.GUI_Q_T2_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=Frame.GUI_Q_T2_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 3 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=Frame.GUI_Q_T3_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=Frame.GUI_Q_T3_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=Frame.GUI_Q_T3_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=Frame.GUI_Q_T3_overweight_batches_num.GetValue()
        GUI_Data["TRIAL"].append(Trial_Data)

        #Trial 4 ------------------------
        Trial_Data={}
        Trial_Data[u"目前口數"]=Frame.GUI_Q_T4_current_pos.GetValue()
        Trial_Data[u"加碼價格"]=Frame.GUI_Q_T4_overweight_price.GetValue()
        Trial_Data[u"加碼口數"]=Frame.GUI_Q_T4_overweight_pos.GetValue()
        Trial_Data[u"分批次數"]=Frame.GUI_Q_T4_overweight_batches_num.GetValue()
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

        import commentjson
        print("Stop_Data=",commentjson.dumps(Stop_Data, indent=4 , sort_keys=True).decode('unicode-escape'))
            

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


