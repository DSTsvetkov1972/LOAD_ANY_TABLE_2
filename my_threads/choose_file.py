from PySide6 import QtWidgets, QtCore
from colorama import Fore
import global_vars 
import pandas as pd
import os
#from functions import from_file_to_csv
from my_functions.main_window import fill_in_table, from_file_to_csv

class OpenFileThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)


    def run(self): 
        if not global_vars.file:
            global_vars.can_load_file = False
            return 

        if os.path.getsize(global_vars.file) == 0:
            print(Fore.MAGENTA,os.path.getsize(global_vars.file))
            global_vars.ui.header_label.setStyleSheet('color: red')              
            global_vars.ui.header_label.setText('Выберите файл для загрузки')
            global_vars.ui.footer_label.setStyleSheet('color: red')                      
            global_vars.cant_load_file_reason = 'Пустой файл не может быть загружен!'
            #global_vars.ui.pushButtonChooseFile.setEnabled(True)            
            global_vars.can_load_file = False 
            #input('ssssssssssss')
        else:
            if global_vars.file[-4:] in ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']:
                print(Fore.YELLOW, 'Мы тут', Fore.RESET)
                try:
                    with pd.ExcelFile(global_vars.file) as excel_file_obj:
                        global_vars.sheet_names = excel_file_obj.sheet_names
                    global_vars.can_load_file = True          
                except ValueError:
                    global_vars.cant_load_file_reason = 'Файл не читается обработчиком эксель-файлов!'
                    global_vars.can_load_file = False                
            else:
                try:
                    global_vars.df = from_file_to_csv(global_vars.file)
                    global_vars.df.index += 1
                    global_vars.can_load_file = True
                except:
                    global_vars.df = pd.DataFrame()
                    global_vars.cant_load_file_reason = 'Файл не читается обработчиком CSV-файлов!'                    
                    global_vars.can_load_file = False

    def on_clicked_choose_file(self):
        #global file
        #if hasattr(self,'comboSheets'):
        global_vars.ui.comboSheets.setVisible(False)
        #    globals.ui.verticalLayoutRight.removeWidget(self.comboSheets)                
        #    delattr(self,'comboSheets')
        global_vars.header_row = 0
        global_vars.ui.tableWidget.setRowCount(0)
        global_vars.ui.tableWidget.setColumnCount(0) 
        global_vars.ui.tableWidget.clear()
        global_vars.file = QtWidgets.QFileDialog.getOpenFileName()[0]      
        self.start() # Запускаем поток  
          
    def on_started_choose_file_thread(self): # Вызывается при запуске потока
        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False) 
        global_vars.ui.err_tableWidget.clear()
        global_vars.ui.err_tableWidget.setVisible(False) 
        global_vars.ui.header_label.setText('')   
        global_vars.ui.footer_label.setStyleSheet('color: blue')       
        global_vars.ui.footer_label.setText(f"Загружаем для предпросмотра {global_vars.file}...")

    ##### не используется так как недоразобрался с видимостью комбобоксов (((    
    def on_finished_choose_file_thread(self): # Вызывается при завершении потока
        if global_vars.can_load_file:
            if global_vars.file[-4:] in ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']:
                #sheet_names = excel_file_obj.sheet_names 
                #self.comboSheets = QtWidgets.QComboBox()
                #globals.ui.verticalLayoutRight.insertWidget(1, self.comboSheets)

                global_vars.ui.comboSheets.currentIndexChanged.connect(global_vars.ui.choose_sheet_thread.df_from_sheet) 

                global_vars.ui.comboSheets.clear()
                for sheet_name in  global_vars.sheet_names:
                    global_vars.ui.comboSheets.addItem(sheet_name)                    
                    #self.comboSheets.setFixedWidth(200)
                print('a')     
            else:
                global_vars.ui.comboSheets.setVisible(False)
                fill_in_table() 
                global_vars.ui.footer_label.setStyleSheet('color: green')                
                global_vars.ui.footer_label.setText(f'Файл {global_vars.file} загружен!')
                print('b') 
            
            print('c')
            global_vars.ui.pushButtonUp.setEnabled(True)             
            global_vars.ui.pushButtonDown.setEnabled(True) 
            global_vars.ui.pushButtonLoader.setEnabled(True) 
            global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(True)            
            global_vars.ui.header_label.setStyleSheet('color: black')              
            global_vars.ui.header_label.setText(f'{global_vars.file}')  
        else:
            global_vars.ui.footer_label.setStyleSheet('color: red')            
            global_vars.ui.footer_label.setText(f'Не удалось загрузить {global_vars.file}. Файл должен быть в формате XLS, XLSX или TSV!') 


        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)
        global_vars.ui.comboSheets.setEnabled(True)           
