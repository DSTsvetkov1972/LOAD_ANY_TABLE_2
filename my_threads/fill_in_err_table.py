from PySide6 import QtCore, QtWidgets
from colorama import Fore
import pandas as pd
import global_vars

class FillInErrTable(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):

        # Заполнить вьюшку
        row_number = 0
        for row in global_vars.err_df.itertuples():
            column_number = 0
            for item in row[2:]:
                cellinfo = QtWidgets.QTableWidgetItem(str(item))
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                global_vars.err_tableWidget.setItem(row_number, column_number, cellinfo)
                column_number += 1
            row_number +=1