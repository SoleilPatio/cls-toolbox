# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


class StockPrice(object):
    def __init__(self):
        self.start = 9800  # 股價開始
        self.end = 7800  # 股價結束

    def GetValues(self):
        values = []
        for price in range(self.start, self.end, 1 if self.end > self.start else -1):
            values.append(price)
        return values


class FuturePosition(object):
    def __init__(self):
        pass

    def ApplyPolicy(self, StockPrice):
        add_range = StockPrice.start * 0.05  # 5% 加碼
        positions = []
        counter = 0
        position = 0
        for price in range(StockPrice.start, StockPrice.end, 1 if StockPrice.end > StockPrice.start else -1):
            counter += 1
            if counter % add_range == 0:
                position += 1
            positions.append(position)

        return positions


if __name__ == '__main__':
    stockprice = StockPrice()
    futureposition = FuturePosition()

    positions = futureposition.ApplyPolicy(stockprice)

    print positions

    # plt.plot(stockprice.GetValues(), ".")
    plt.plot(positions, "-")
    plt.show()
    print "\nDonw"
