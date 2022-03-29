#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import xlwings

def ExcelForceUpdate(excel_filename):
    app = xlwings.App(visible=False)
    book = app.books.open(excel_filename)
    book.save(excel_filename)
    book.close()
    app.kill()



