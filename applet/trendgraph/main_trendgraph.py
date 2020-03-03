'''
Created on 2017/5/31

@author: clouds
'''
import numpy as np

class ChartLine(object):
    def __init__(self):
        self.values = None
        self.label = None
        pass
    
    def initlineCompoundInterest(self, PV, rate, n):
        if n < 0:
            self.values = None
            return
        
        self.values = np.zeros(n+1)
        self.values[0] = PV
        
        
        for t in range(1,n+1):
            self.values[t] = self.values[t-1]*(1+rate)
            
        if self.label == None:
            self.label = str(int(rate*100)) + "%"
            
    """
    rate : year rate
    n : year
    """
    def initlinePMT(self, PV, rate, n):
        if n < 0:
            self.values = None
            return
        
        #monthly payment
        p_and_i = np.pmt(rate/12, 12*n, PV)
        p_mon = np.ppmt(rate/12, 0, 12*n, PV)
        i_mon = np.ipmt(rate/12, 0, 12*n, PV)
        
        print p_and_i , p_mon, i_mon , p_mon+i_mon
        
        self.values = np.zeros(12*n+1)
        self.values[0] = 0
        for t in range(1,12*n+1):
            self.values[t] = self.values[t-1] + (-p_and_i)
            
        if self.label == None:
            self.label = str(int(rate*100)) + "%"
            
    def plot_values(self):
        return self.values
    
    def plot_label(self):
        return self.label
    

import matplotlib.pyplot as plt
class Canvas(object):
    def __init__(self):
        pass
    
    def Plot(self, plotable):
        plt.plot(plotable.plot_values(),label=plotable.plot_label())
        
    def Plots(self, plotables):
        for p in plotables:
            self.Plot(p)
        
    def Show(self):
#         fig, ax = plt.subplots()
        plt.grid(True, zorder=5)
#         plt.legend(loc='upper center', shadow=True)
        plt.legend()
        plt.show()
        
        



if __name__ == '__main__':
#     canvas = Canvas()
#     
#     lines = [ ChartLine() for _ in range(10) ]
#     
#     for i, l in enumerate(lines):
#         l.initlineCompoundInterest(1, (i+1)*0.02/12, 20*12)
#       
#       
#     invest_line = ChartLine()
#     invest_line.initlineCompoundInterest(1, 0.05/12, 20*12)
#     
#     pmt_line = ChartLine()
#     pmt_line.initlinePMT(1, 0.015, 20)
#     
#     
#     
#     
# #     canvas.Plots(lines)
#     canvas.Plot(invest_line)
#     canvas.Plot(pmt_line)
#     
#     canvas.Show()

    numbers = [1]
    
    for i in range(5):
        n = numbers[i]*1.618
        numbers.append(n)
        
    sums = []
    sum = 0
    for n in numbers:
        sum = sum + n
        sums.append(sum)
    
    print numbers
    
    plt.plot(numbers,".-")
    plt.plot(sums,"x-")
    plt.show()
    print "\nDone"
    pass