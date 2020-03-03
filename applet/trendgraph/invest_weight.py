# -*- coding: utf-8 -*-
import numpy as np

def Invest_Weight(start_pa, end_pa, num):
    """
    1+2+3
    """
    pa_list = np.linspace(start_pa, end_pa, num=num)
    
    print pa_list
    print pa_list.sum()

def to_excel(list):
    return '\t'.join([ "%.2f"%_ for _ in list ])
    

def h2l_l2h(a_per, b_per, bin_num):
    down_percentages = np.linspace(a_per, b_per, num=bin_num)
    print "下跌%=\t",to_excel(down_percentages)
    
    prices = 1*(1+down_percentages)
    print "價格 =\t",to_excel(prices)
    
    up_percentages = []
    _base = prices[-1]
    for p in prices:
        up_percentages.append((p-_base)/_base)
    print "上漲% =\t",to_excel(up_percentages)
        
    


def ratios(nums):
    ratios = []
    max = (nums[0],0)
    min = (nums[0],0)
    for i in range(1, len(nums)):
        a = float(nums[i-1])
        b = float(nums[i])
        
        r = (b-a)/a
        ratios.append(r)
        
        if b > max[0]:
            max = (b , i)
        if b < min[0]:
            min = (b , i)
        
    #whole_ratio
    if max[1] < min[1]:
        whole_ratio = (min[0]-max[0])/max[0]
    else:
        whole_ratio = (max[0]-min[0])/min[0]
        
    print min
    print max
        
    print "whole_ratio=",whole_ratio
    return ratios 
        
    
    
    



if __name__ == "__main__":
    h2l_l2h(0, -0.6, 5+1)
    
    ra = ratios([55.07,41.7,50,43.3,48.31,25.05,31.63,28.74])
    print to_excel(ra)
    
    a = ratios([
        91.05,
        83.28,
        100.564,
        90.24,
        106.245,
        99.75,
        109.42,
        104.34,
        114.39,
        84.74,
        115.75,
        94.84,
        111.33,
        104.54,
        110.75,
        101.75,
        119.48,
        113.45
        ])
    
    b = ["%.02f"%_ for _ in sorted(a)]
    print b
     
    
    print "Done"