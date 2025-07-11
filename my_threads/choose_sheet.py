from PySide6 import QtCore
import pandas as pd
import global_vars
from my_functions.main_window import fill_in_table
from colorama import Fore

class ChooseSheetThread(QtCore.QThread):
    def __init__ (self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        self.header_row = 0
        print(Fore.RED, 'Мы тут', Fore.RESET)
        global_vars.df = pd.read_excel(global_vars.file, header = None, dtype= 'string', engine = 'calamine', sheet_name = global_vars.sheet_name, nrows = 15)
        print(global_vars.df)
        
        if not global_vars.df.empty:
            global_vars.df.fillna('', inplace = True)
            global_vars.df.index += 1
            global_vars.df.can_load_file = True
            global_vars.loaded_file = ''       
            global_vars.loaded_sheet_name = ''

    def starter(self):
        #global sheet_name_global
        #sheet_name_global = globals.ui.comboSheets.currentIndex()

        global_vars.sheet_name = global_vars.ui.comboSheets.currentText()
        global_vars.header_row = 0 
        global_vars.ui.tableWidget.setRowCount(0)
        global_vars.ui.tableWidget.setColumnCount(0) 
        global_vars.ui.tableWidget.clear()   
       
        self.start()   # Запускаем поток  



    def on_started(self): # Вызывается при запуске потока
        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False)         
        global_vars.ui.err_tableWidget.setVisible(False) 
        global_vars.ui.footer_text.setVisible(False)   
        global_vars.ui.footer_label.setStyleSheet('color: blue')                       
        global_vars.ui.footer_label.setText(f'Загружаем несколько начальных строк листа "{global_vars.ui.comboSheets.currentText()}" для предпросмотра...')

    
    def on_finished(self): # Вызывается при завершении потока
        if not global_vars.df.empty:
            fill_in_table()
            global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)
            global_vars.ui.pushButtonUp.setEnabled(True)
            global_vars.ui.pushButtonDown.setEnabled(True)             
            global_vars.ui.pushButtonLoader.setEnabled(True)
            global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(True)        
            global_vars.ui.comboSheets.setEnabled(True)          
            global_vars.ui.comboSheets.setVisible(True)    
            global_vars.ui.footer_label.setStyleSheet('color: green')                
            global_vars.ui.footer_label.setText(f'Несколько начальных строк листа "{global_vars.ui.comboSheets.currentText()}" загружены для предпросмотра, заголовки - номера столбцов!')
        else:
            global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)
            global_vars.ui.pushButtonUp.setEnabled(False)
            global_vars.ui.pushButtonDown.setEnabled(False)      
            global_vars.ui.pushButtonLoader.setEnabled(False)
            global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(False)               
            global_vars.ui.comboSheets.setEnabled(True)          
            global_vars.ui.comboSheets.setVisible(True)    
            global_vars.ui.footer_label.setStyleSheet('color: red')                
            global_vars.ui.footer_label.setText(f'Лист "{global_vars.ui.comboSheets.currentText()}" - пустой!')
