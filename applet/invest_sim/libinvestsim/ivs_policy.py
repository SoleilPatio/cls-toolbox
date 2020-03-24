# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from libcommon.json_config import JsonConfig


class IvsPolicy(object):
    def __init__(self):
        super(IvsPolicy, self).__init__()

    def CalProduct(self, product_dict , update_input_dict=True ):
        ret = {
            u"回合停損淨值": [],
            u"回合可損失淨值":  [],
            u"回合口數試算": [],
            u"當日已損失淨值": [],
            u"當日剩餘可損失淨值": [],
            u"當日剩餘可損失淨值%": [],
            u"當日停損價": [],
            u"當日停損%": [],
            u"當日口數試算": [],
            u"當日停損淨值": []
        }

        # 產品規格
        margin = float(product_dict[u"保證金"])
        multiplier = float(product_dict[u"乘數"])

        # 對每個日期做處理
        for index, date in enumerate(product_dict[u"日期"]):
            run_max_netvalue = float(product_dict[u"回合最大淨值"][index])
            stoploss_rate = float(product_dict[u"可損失比率"][index])
            netvalue = float(product_dict[u"當日淨值"][index])
            price = float(product_dict[u"當日市價"][index])
            position = int(product_dict[u"當日口數"][index])
            sign = 1 if position >= 0 else -1   #做多或做空

            run_stoploss_netvalue = run_max_netvalue*(1-stoploss_rate)  #停損淨值，以回合最大淨值計算，停損部分回合或當日，以回合爲準
            ret[u"回合停損淨值"].append(run_stoploss_netvalue)

            run_stoploss_netvalue_quota = run_max_netvalue*stoploss_rate
            ret[u"回合可損失淨值"].append(run_stoploss_netvalue_quota)

            netvalue_loss = run_max_netvalue - netvalue     #當日爲止已損失多少淨值，負數爲賺
            ret[u"當日已損失淨值"].append(netvalue_loss)

            #還有多少可以損失,netvalue_loss < 0則不計
            if netvalue_loss >= 0:
                stoploss_netvalue_quota_remain = run_stoploss_netvalue_quota - netvalue_loss
            else:
                stoploss_netvalue_quota_remain = run_stoploss_netvalue_quota # 表示quota都沒用到，都還沒賠到
            ret[u"當日剩餘可損失淨值"].append(stoploss_netvalue_quota_remain)


            stoploss_netvalue_quota_remain_ratio = stoploss_netvalue_quota_remain/run_stoploss_netvalue_quota #剩餘損失百分比，>1 表示賺
            ret[u"當日剩餘可損失淨值%"].append(stoploss_netvalue_quota_remain_ratio*100)

            stoploss_point = 0 - ( stoploss_netvalue_quota_remain*1000 / (position*multiplier) )  # 依照目前口數下，可以跌幾點
            ret[u"當日停損價"].append(price + stoploss_point)

            stoploss_ratio = stoploss_point/price  # 依照目前口數下，可以跌幾%
            ret[u"當日停損%"].append(stoploss_ratio*100)

            stoploss_netvalue = netvalue - stoploss_netvalue_quota_remain  # 依照目前口數，當日停損在哪一個淨值
            ret[u"當日停損淨值"].append(stoploss_netvalue)



            # 回合口數試算: 計算口數組合與漲跌幅度的關係
            comb_list = []  # list of multiple dicts, one dict for a combination
            pos = 1*sign
            while True :
                stoploss_point = 0 - ( run_stoploss_netvalue_quota*1000 / (pos*multiplier) )  # 限定口數下，可以跌幾點
                stoploss_ratio =  stoploss_point/price  # %數
                if abs(stoploss_ratio) < 0.02:  #< 2% 太投機不看
                    break
                comb = {}
                comb[u"口數"] = pos
                comb[u"停損價"] = price + stoploss_point
                comb[u"停損點數"] = stoploss_point
                comb[u"停損%"] = stoploss_ratio*100
                comb_list.append(comb)
                pos += sign*1

            ret[u"回合口數試算"].append(comb_list)


            # 當日口數試算: 計算口數組合與漲跌幅度的關係
            comb_list = []  # list of multiple dicts, one dict for a combination
            pos = 1*sign
            while True :
                stoploss_point = 0 - ( stoploss_netvalue_quota_remain*1000 / (pos*multiplier) )  # 限定口數下，可以跌幾點
                stoploss_ratio =  stoploss_point/price  # %數
                if abs(stoploss_ratio) < 0.02:  #< 2% 太投機不看
                    break
                comb = {}
                comb[u"口數"] = pos
                comb[u"停損價"] = price + stoploss_point
                comb[u"停損點數"] = stoploss_point
                comb[u"停損%"] = stoploss_ratio*100
                comb_list.append(comb)
                pos += sign*1

            ret[u"當日口數試算"].append(comb_list)



        #更新到主資料庫
        if update_input_dict is True:
            product_dict.update(ret)

        

        return ret


    """
    回傳Product的物件，只保留最近一天的資料
    """
    def UtilKeepOnlyLatestRecord(self, product_dict):
        ret = {}
        for key in product_dict:
            if type(product_dict[key]) is list:
                ret[key]=[product_dict[key][-1]] if len(product_dict[key]) else []
            else:
                ret[key]=product_dict[key]
        return ret



if __name__ == '__main__':
    pass
