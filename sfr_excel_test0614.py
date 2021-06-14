# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 17:59:10 2021

@author: Sean Ruane
"""

import win32com.client
from PIL import ImageGrab
import os
from openpyxl import load_workbook

file_loc = "C:\\Users\\Sean Ruane\\Documents\\"

try:
#    wb = load_workbook(file_loc + 'phi_summary_raw.xlsx')
#    ws = wb.active
#    ws.insert_rows(41, 3)
#    ws.insert_rows(77, 3)
#    ws.insert_rows(104, 3)
#
#    wb.save(file_loc + 'phi_summary_raw3.xlsx')
    
    o = win32com.client.gencache.EnsureDispatch("Excel.Application")
    wb = o.Workbooks.Open(file_loc + 'phi_summary_raw2.xlsx') # phi_summary_raw3.xlsx
    ws = wb.Worksheets("sheet1")

    ws.Range(ws.Cells(1, 1), ws.Cells(40, 14)).CopyPicture(Format=win32com.client.constants.xlBitmap)
    img = ImageGrab.grabclipboard()
    imgFile = os.path.join(os.getcwd(), file_loc + 'S1.png')
    img.save(imgFile)

    ws.Range(ws.Cells(41, 1), ws.Cells(76, 14)).CopyPicture(Format=win32com.client.constants.xlBitmap)
    img = ImageGrab.grabclipboard()
    imgFile = os.path.join(os.getcwd(), file_loc + 'S2.png')
    img.save(imgFile)

    ws.Range(ws.Cells(77, 1), ws.Cells(103, 14)).CopyPicture(Format=win32com.client.constants.xlBitmap)
    img = ImageGrab.grabclipboard()
    imgFile = os.path.join(os.getcwd(), file_loc + 'S3.png')
    img.save(imgFile)

    ws.Range(ws.Cells(104, 1), ws.Cells(149, 14)).CopyPicture(Format=win32com.client.constants.xlBitmap)
    img = ImageGrab.grabclipboard()
    imgFile = os.path.join(os.getcwd(), file_loc + 'S4.png')
    img.save(imgFile)

    wb.Close()
except AttributeError:
    # Corner case dependencies.
    import os
    import re
    import sys
    import shutil
    # Remove cache and try again.
    MODULE_LIST = [m.__name__ for m in sys.modules.values()]
    for module in MODULE_LIST:
        if re.match(r'win32com\.gen_py\..+', module):
            del sys.modules[module]
    shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
    from win32com import client
    o = client.gencache.EnsureDispatch('Excel.Application')
    
