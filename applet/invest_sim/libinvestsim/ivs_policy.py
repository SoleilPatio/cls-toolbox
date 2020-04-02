# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import logging
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
Sn(num) = 1+2+3+...num
"""
def Sn(num):
    return sum(range(1,num+1))



"""
剩餘可以損失的淨值，不可大於這個回合的初始設定損失淨值
"""
def Remain_Loss_Netvalue( run_max_netvalue, max_loss_rate, current_netvalue):
    loss_netvalue = max(run_max_netvalue - current_netvalue, 0)
    remain_loss_netvalue = run_max_netvalue*max_loss_rate - loss_netvalue
    return remain_loss_netvalue



"""
剩餘可以損失的淨值，不可大於這個回合的初始設定損失淨值
從預期加碼點開始算(少算了從目前價位到預期加碼點之間的損失)
    sign: 1:long -1:short
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
CalcStopPrice():
    max_netvalue:       最大淨值
    current_netvalue：  目前淨值
    max_loss_rate:      可損失比率
    multiplier:         (產品)乘數
    current_price:      目前價格
    overweight_price:   (第一次)加碼價格
    current_pos:        目前口數
    overweight_pos:     加碼口數
    num_batches:        分批次數
"""
def CalcStopPrice(  max_netvalue, current_netvalue, max_loss_rate, 
                    multiplier, 
                    current_price, overweight_price,
                    current_pos, overweight_pos, num_batches ):
    ret = {}

    #[Sanity Test]
    assert max_netvalue >= current_netvalue
    assert num_batches >= 1
    # assert abs(extra_pos) >= num_batches

    #如果沒有填寫加碼價格，預設目前價格加碼
    if overweight_price == 0:
        overweight_price = current_price

    #[Long or Short]
    if current_pos > 0: #做多或做空
        sign = 1
    elif current_pos < 0:
        sign = -1
    elif overweight_pos > 0:
        sign = 1
    elif overweight_pos < 0:
        sign = -1
    else:
        logging.error("sign unknown!")
        return None
        assert sign

    #[Start Calculate]
    max_loss_net = max_netvalue * max_loss_rate
    ret[u"最大損失淨值"]=max_loss_net
    logging.debug("max_loss_net (最大損失淨值)=%s"%max_loss_net)
    

    remain_loss_netvalue = Remain_Loss_Netvalue(max_netvalue, max_loss_rate, current_netvalue)
    ret[u"剩餘可損失淨值"]=remain_loss_netvalue
    logging.debug("remain_loss_net (剩餘可損失淨值)=%s"%remain_loss_netvalue )

    remain_loss_netvalue_from_overweight = Remain_Loss_Netvalue_From_Overweight(sign, remain_loss_netvalue, current_price, overweight_price, multiplier, current_pos)
    logging.debug("remain_loss_netvalue_from_overweight (剩餘可損失淨值_從加碼點)=%s"%remain_loss_netvalue_from_overweight )
    if remain_loss_netvalue_from_overweight < 0:
        logging.error("remain_loss_netvalue_from_overweight < 0 : 剩餘可損失淨值 < 0 , 可能已經打到停損")
        return None
        assert remain_loss_netvalue_from_overweight  >= 0

    remain_loss_points = remain_loss_netvalue_from_overweight / multiplier #可損失點數
    logging.debug("remain_loss_points (剩餘損失點數)=%s"%remain_loss_points)

    num_pos_per_batch = overweight_pos/num_batches
    ret[u"每次加碼口數"]=num_pos_per_batch
    logging.debug("num_pos_per_batch (每次加碼口數)=%s"%num_pos_per_batch)

    a_coef = num_pos_per_batch*Sn(num_batches) + current_pos*num_batches
    ret[u"a係數"]=a_coef
    logging.debug("a_coef (a係數)=%s"%a_coef)

    sec_point = (0 - remain_loss_points/a_coef)
    ret[u"加碼間隔"]=sec_point
    logging.debug("sec_point (加碼間隔)=%s"%sec_point)

    sec_percentage = sec_point/current_price
    ret[u"加碼間隔%"]=sec_percentage*100
    logging.debug("sec_percentage (加碼間隔%%)=%s"%(sec_percentage*100))

    stop_points = sec_point*num_batches + ( overweight_price - current_price )
    ret[u"停損點數"]=stop_points
    logging.debug("stop_points (停損點數)=%s"%stop_points)

    stop_points_percentage = stop_points/current_price
    ret[u"停損點數%"]=stop_points_percentage*100
    logging.debug("stop_points_percentage (停損點數%%)=%s"%(stop_points_percentage*100))

    #加碼點(最後一個永遠是停損點)
    ret[u"各次加碼價格"]=[]
    logging.debug("各次加碼價格:")
    for i in range(num_batches):
        price = overweight_price + i*sec_point
        ret[u"各次加碼價格"].append(price)
        logging.debug("\t%d:%d" % (i, price))
    price =  overweight_price + num_batches*sec_point
    ret[u"各次加碼價格"].append(price)
    ret[u"停損價格"]=price
    logging.debug("\t%d:%d(STOP)" % (num_batches, overweight_price + num_batches*sec_point))

    return ret

# end of CalcStopPrice()





def TEST_CalcStopPrice():
    #[User-Input]
    k=1000
    max_netvalue = 26.81*k
    current_netvalue = 25.45*k

    max_loss_rate = 0.1
    multiplier = 1               #乘數

    current_price = 12675
    # overweight_price = 12800   #第一次加碼價位
    overweight_price = 12675

    current_pos = -4 #目前口數
    overweight_pos = 0   #想要再加幾口
    num_batches = 1 #分幾次下單

    #Call core function
    ret = CalcStopPrice(  max_netvalue, current_netvalue, max_loss_rate, 
                    multiplier, 
                    current_price, overweight_price,
                    current_pos, overweight_pos, num_batches )

    print(str(ret).decode('unicode-escape'))


 


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_CalcStopPrice()
    pass
