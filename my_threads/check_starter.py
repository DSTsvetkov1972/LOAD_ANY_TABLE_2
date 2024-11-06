'''
Модуль содержит фунции, которые проверяют данные в колонке загружаемой таблицы (df)
на соответствие формату.
Функции запускаются из объекта класса 
'''
import global_vars
from colorama import Fore
from pandas import DataFrame, concat
from PySide6 import QtWidgets, QtCore, QtGui
from time import sleep
import pandas as pd
import my_functions.checks as fnc


class CheckStarterThread(QtCore.QThread):
    '''
    Поток стартующий при запуски проверки. Для каждого comboSheets создаётся свой поток
    '''
    mysignal = QtCore.Signal(tuple)  
    def __init__ (self, combo, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.checks_dict ={'String' : fnc.check_String,
                    'DateOrNull'    : fnc.check_DateTimeOrNull,
                    'DateTimeOrNull': fnc.check_DateTimeOrNull,
                    'Int32OrNull'   : fnc.check_Int32OrNull,
                    'Float32OrNaN'  : fnc.check_Float32OrNaN,
                    'Date'          : fnc.check_DateTime,
                    'DateTime'      : fnc.check_DateTime,
                    'Int32'         : fnc.check_Int32,
                    'Float32'       : fnc.check_Float32,
                    'Container'     : fnc.check_Container,
                    'Vagon'         : fnc.check_Vagon} 
        self.combo = combo
        self.header_row = global_vars.header_row
        self.column_number = self.combo.column_number
        

        self.no_errs_df = DataFrame(columns = ['column_number','Сообщение','Ячейка LN','Ячейка RNCN','Значение'])
        global_vars.ui.checks_result_df = self.no_errs_df 
    
    def fill_in_err_table(self):
        global_vars.ui.err_tableWidget.setRowCount(len(global_vars.ui.checks_result_df))
        global_vars.ui.err_tableWidget.setColumnCount(4)  
        
        global_vars.ui.err_tableWidget.setHorizontalHeaderLabels(['Ошибка','Ячейка','Ячейка','Значение'])
        #ui.tableWidget.setVerticalHeaderLabels(self.verticalHeaders)
        
        # Заполнить вьюшку
        print('начали заполнять вьюшку')
        row_number = 0
        for row in global_vars.ui.checks_result_df.itertuples():
            column_number = 0
            for item in row[2:]:
                cellinfo = QtWidgets.QTableWidgetItem(str(item))
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
                )
                global_vars.ui.err_tableWidget.setItem(row_number, column_number, cellinfo)
                column_number += 1
            row_number +=1
            #if row_number % 100:
            #   print(row_number)
            
            sleep(0.00000001)
            self.mysignal.emit(('fill_in_err_table', row_number, len(global_vars.ui.checks_result_df))) 
        print('ПОКОНЧИЛИ заполнять вьюшку')


    def run(self):
        sleep(0.1)
        global_vars.ui.checks_started_qty += 1

   
        self.combo.load_file_sheet_name()
        
        global_vars.ui.footer_label.setStyleSheet('color: green')                      
        global_vars.ui.footer_label.setText(f'Весь лист "{global_vars.ui.comboSheets.currentText()}" загружен!')
    

        global_vars.ui.checks_result_df = global_vars.ui.checks_result_df[global_vars.ui.checks_result_df['column_number'] != self.column_number]     
        self.result = self.checks_dict.get(self.combo.currentText())(global_vars.df[self.column_number], self.combo.column_number, global_vars.header_row, self.mysignal)
        global_vars.ui.checks_result_df = concat([global_vars.ui.checks_result_df, self.result[0]]) 
        
        #self.combo.setStyleSheet(self.result[1]) 
        global_vars.check_result_style_sheet = self.result[1]      
        
        self.all_err_df = concat([global_vars.ui.checks_result_df, self.result[0]]) 
        global_vars.ui.checks_started_qty -= 1  

        if global_vars.ui.checks_started_qty == 0:           

            if global_vars.ui.checks_result_df.empty:
                print(Fore.GREEN,'Мы здесь', Fore.WHITE)
                sleep(0.1) 
                global_vars.ui.footer_label.setStyleSheet('color: green')             
                global_vars.ui.footer_label.setText('Все проверки завершены, ошибки форматирования не найдены!') 
                sleep(0.1)   
                global_vars.ui.pushButtonLoader.setEnabled(True)
                global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(True)                
            else:
                global_vars.ui.footer_label.setStyleSheet('color: blue')                
                global_vars.ui.footer_label.setText('Подготавливаем к выводу список ошибок...')
                self.fill_in_err_table()
                #self.fill_in_err_table_cls()   
                global_vars.ui.err_tableWidget.resizeColumnsToContents()                
                sleep(0.1)
                global_vars.ui.footer_label.setStyleSheet('color: red')                
                global_vars.ui.footer_label.setText('Все проверки завершены, имеются ошибки форматирования!') 
                print('Таблица с ошибками готова')
                #sleep(0.1)
                global_vars.ui.pushButtonLoader.setEnabled(False)
                global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(False)
                global_vars.ui.err_tableWidget.setVisible(True)

            global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)           
            global_vars.ui.comboSheets.setEnabled(True)
            global_vars.checks_dict = {}  
        #sleep(0.1)
        print(f'Проверка run  окончена {global_vars.check_result_style_sheet}')