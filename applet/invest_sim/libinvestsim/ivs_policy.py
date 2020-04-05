# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import logging
import libcommon.utilities as util
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


# end of IvsPolicy

"""
--------------------------------------------------------
Sn(num) = 1+2+3+...num
--------------------------------------------------------
"""
def Sn(num):
    return sum(range(1,num+1))


"""
--------------------------------------------------------
剩餘可以損失的淨值，不可大於這個回合的初始設定損失淨值
--------------------------------------------------------
"""
def Remain_Loss_Netvalue( run_max_netvalue, max_loss_rate, current_netvalue):
    loss_netvalue = max(run_max_netvalue - current_netvalue, 0)
    remain_loss_netvalue = run_max_netvalue*max_loss_rate - loss_netvalue
    return remain_loss_netvalue


"""
--------------------------------------------------------
剩餘可以損失的淨值，不可大於這個回合的初始設定損失淨值
從預期加碼點開始算(少算了從目前價位到預期加碼點之間的損失)
    sign: 1:long -1:short
--------------------------------------------------------
"""
def Remain_Loss_Netvalue_From_Overweight(   sign, remain_loss_netvalue, 
                                            current_price, overweight_price, multiplier, current_pos ):
    if sign:
        loss_points = current_price - overweight_price
    else:
        loss_points = overweight_price - current_price
    remain_loss_netvalue_from_overweight =  remain_loss_netvalue - loss_points*multiplier*current_pos
    return remain_loss_netvalue_from_overweight



"""
--------------------------------------------------------
加碼數列
    is_policy_aggressive:
            True: 分次除不盡時傾向先加碼
            False:分次除不盡時傾向後加碼
--------------------------------------------------------
"""
def Avg_Buy_Pos_List(avg_buy_pos, avg_buy_count, is_policy_aggressive):
    ret = []
    sign = 1 if avg_buy_pos >=0 else -1 #做多或做空

    remain_count = abs(avg_buy_pos)%avg_buy_count
    
    if is_policy_aggressive:
        remain_list = [sign*1] * (remain_count) + [0]*(avg_buy_count-remain_count)
    else:
        remain_list = [0]*(avg_buy_count-remain_count) + [sign*1] * (remain_count)

    ret = [sign*(abs(avg_buy_pos)/avg_buy_count)] * avg_buy_count
    ret = map(lambda x,y: x+y, ret, remain_list)

    return ret

"""
--------------------------------------------------------
各加碼點的總口數 list
    buy_pos_list := Avg_Buy_Pos_List(avg_buy_pos, avg_buy_count, is_policy_aggressive)
--------------------------------------------------------
"""
def Avg_Buy_Total_Pos_List(buy_pos_list, current_pos):
    ttl_pos_list = [current_pos]
    for buy_pos in buy_pos_list:
        ttl_pos_list.append(ttl_pos_list[-1]+buy_pos)
    del ttl_pos_list[0]
    return ttl_pos_list

"""
--------------------------------------------------------
A-coef calculation
--------------------------------------------------------
"""
def A_Coef(buy_pos_list, current_pos):
    ttl_pos_list = Avg_Buy_Total_Pos_List(buy_pos_list, current_pos)
    a_coef = reduce(lambda x,y: x+y, ttl_pos_list)
    return a_coef



"""
--------------------------------------------------------
CalcStopPrice():
    max_netvalue:       最大淨值
    current_netvalue：  目前淨值
    max_loss_rate:      可損失比率
    multiplier:         (產品)乘數
    current_price:      目前價格
    avg_buy_price:      (第一次)加碼價格
    current_pos:        目前口數
    avg_buy_pos:        加碼口數
    avg_buy_count:      分批次數
    is_policy_aggressive:
            True: 分次除不盡時傾向先加碼
            False:分次除不盡時傾向後加碼
--------------------------------------------------------
"""
def CalcStopPrice(  max_netvalue, current_netvalue, max_loss_rate, 
                    multiplier, 
                    current_price, avg_buy_price,
                    current_pos, avg_buy_pos, avg_buy_count,
                    is_policy_aggressive = True ):
    ret = {}

    #[Sanity Test]
    if not max_netvalue >= current_netvalue:
        logging.error("max_netvalue(%d) < current_netvalue(%d)"%(max_netvalue,current_netvalue))
        return
    if not avg_buy_count >= 1:
        logging.error("avg_buy_count(%d) < 1"%(avg_buy_count))
        return

    #如果沒有填寫加碼價格，預設目前價格加碼
    if avg_buy_price == 0:
        avg_buy_price = current_price

    #[Long or Short]
    if current_pos > 0: #做多或做空
        sign = 1
    elif current_pos < 0:
        sign = -1
    elif avg_buy_pos > 0:
        sign = 1
    elif avg_buy_pos < 0:
        sign = -1
    else:
        logging.error("sign unknown! (current_pos(%d) ,avg_buy_pos(%d))" % (current_pos, avg_buy_pos))
        return None

    #[Start Calculate]
    max_loss_net = max_netvalue * max_loss_rate
    ret[u"最大損失淨值"]=max_loss_net
    

    remain_loss_netvalue = Remain_Loss_Netvalue(max_netvalue, max_loss_rate, current_netvalue)
    ret[u"剩餘可損失淨值"]=remain_loss_netvalue

    remain_loss_netvalue_from_overweight = Remain_Loss_Netvalue_From_Overweight(sign, remain_loss_netvalue, current_price, avg_buy_price, multiplier, current_pos)
    if remain_loss_netvalue_from_overweight < 0:
        logging.error("remain_loss_netvalue_from_overweight < 0 : 剩餘可損失淨值 < 0 , 可能已經打到停損")
        return None

    remain_loss_points = remain_loss_netvalue_from_overweight / multiplier #可損失點數

    
    ret[u"各次加碼口數"]=Avg_Buy_Pos_List(avg_buy_pos, avg_buy_count, is_policy_aggressive)
    ret[u"各次加碼總口數"]=Avg_Buy_Total_Pos_List(ret[u"各次加碼口數"], current_pos)

    a_coef = A_Coef(ret[u"各次加碼口數"], current_pos)
    ret[u"a係數"]=a_coef

    # a_coef 爲0 ,發生在回補以後清倉
    if a_coef == 0:
        logging.error("a_coef=0! 目前口數:%d 各次加碼口數:%s"%(current_pos, ret[u"各次加碼口數"]))
        return

    sec_point = (0 - remain_loss_points/a_coef)
    ret[u"加碼間隔"]=sec_point

    sec_percentage = sec_point/current_price
    ret[u"加碼間隔%"]=sec_percentage*100

    stop_points = sec_point*avg_buy_count + ( avg_buy_price - current_price )
    ret[u"停損點數"]=stop_points

    stop_points_percentage = stop_points/current_price
    ret[u"停損點數%"]=stop_points_percentage*100

    #加碼點(最後一個永遠是停損點)
    ret[u"各次加碼價格"]=[]
    for i in range(avg_buy_count):
        price = avg_buy_price + i*sec_point
        ret[u"各次加碼價格"].append(price)
    price =  avg_buy_price + avg_buy_count*sec_point
    ret[u"各次加碼價格"].append(price)
    ret[u"停損價格"]=price

    #其他資訊
    ret[u"多空"]=sign
    

    return ret

# end of CalcStopPrice()



def TEST_CalcStopPrice():
    #[User-Input]
    k=1000
    max_netvalue = 300.0*k
    current_netvalue = 290.0*k

    max_loss_rate = 0.1
    multiplier = 1               #乘數

    current_price = 12500
    # overweight_price = 12800   #第一次加碼價位
    avg_buy_price = 12500

    current_pos = 4        #目前口數
    avg_buy_pos = 6      #想要再加幾口
    avg_buy_count = 4         #分幾次下單

    #Call core function
    ret = CalcStopPrice(  max_netvalue, current_netvalue, max_loss_rate, 
                    multiplier, 
                    current_price, avg_buy_price,
                    current_pos, avg_buy_pos, avg_buy_count )

    print(util.StrObj(ret))


 


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_CalcStopPrice()

    # print( Avg_Buy_Pos_List(6, 4, True) )
    # print( Avg_Buy_Pos_List(-6, 4, False) )

    # print(A_Coef(Avg_Buy_Pos_List(6, 4, True), 4))
    pass
