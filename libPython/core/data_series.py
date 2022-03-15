# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy
from collections import OrderedDict


class DataSeries(object):
    def __init__(self) -> None:
        self.m_series = OrderedDict()
        pass

    def __str__(self) -> str:
        ret = ""
        for idx, s in enumerate(self.m_series):
            # ret += f"{type(self.m_series[s]).__name__}:{s}({self.m_series[s].size})={str(self.m_series[s])}\n"
            ret += f"[{idx}]:{s}({self.m_series[s].size})={str(self.m_series[s])}\n"
        return ret

    def series(self, name):
        return self.m_series[name]

    def size(self):
        try:
            return self.series_by_index(0).size
        except:
            return 0

    def series_by_index(self, idx):
        return self.m_series[list(self.m_series.keys())[idx]]

    def add_series(self, name, values):
        self.m_series[name] = numpy.array(values)

    def link_series(self, name, target_np_array):
        if isinstance(target_np_array, numpy.ndarray):
            self.m_series[name] = target_np_array
            return True
        else:
            print("error: only np array can be linked.")
            return False


"""
-----------------------------------------------
Main Test
-----------------------------------------------
"""
if __name__ == '__main__':
    ds = DataSeries()
    print(ds)
    ds.add_series("x", [1, 2, 3, 4])
    ds.add_series("y", [4, 5, 6, 7, 8])
    ds.link_series("z", ds.series("x"))
    # ds.link_series("w", [1,2,3])
    print(ds)
    ds.series("x")[0] = 999
    print(ds)
    print(ds.series("x"))
    print(ds.series_by_index(0))
    ds.series_by_index(0)[0] = 888
    print(ds)
    print("Done.")
