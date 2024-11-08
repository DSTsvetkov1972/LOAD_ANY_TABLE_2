from PySide6 import QtWidgets, QtCore
from my_windows import main_window, log_in_dialog
import global_vars
import pandas as pd
from my_functions.main_window import header_down, fill_in_table, translit
from my_functions.dwh import log_out, get_params, connection_settings_file_creator
import re
from colorama import Fore



from my_threads.load_in_dwh import LoadInDWHThread
from my_threads.choose_file import OpenFileThread
from my_threads.choose_sheet import ChooseSheetThread
from my_threads.header_up import HeaderUpThread
from my_threads.log_in_check import LogInCheck

class LogInDialog(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = log_in_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.log_in_check_thread.start()  
        params = get_params()
        self.ui.lineEditHostField.setText(params[0])         
        self.ui.lineEditPortField.setText(params[1])         
        self.ui.lineEditDBNameField.setText(params[2])         
        self.ui.lineEditUserField.setText(params[3])         
        self.ui.lineEditPasswordField.setText(params[4])  
    




    def accept(self):
        connection_settings_file_creator(self.ui.lineEditHostField.text(),
               self.ui.lineEditPortField.text(),
               self.ui.lineEditDBNameField.text(),
               self.ui.lineEditUserField.text(),
               self.ui.lineEditPasswordField.text()
               )
        self.log_in_check_thread.start()

    #######################################################################
    #######################################################################   
    log_in_check_thread = LogInCheck() # создаём поток проверки подключения     

class MyWindow(QtWidgets.QWidget):
    def __init__ (self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        global_vars.ui = main_window.Ui_MainWindow()
        global_vars.ui.setupUi(self) 
        self.log_in_check_thread.start()

        global_vars.ui.action_log_in.triggered.connect(self.show_log_in_dialog)
        global_vars.ui.action_log_in_check.triggered.connect(lambda: self.log_in_check_thread.start())          
        global_vars.ui.action_log_out.triggered.connect(log_out)   

        global_vars.ui.action_show_manual.triggered.connect(self.show_manual)   

        global_vars.ui.action_show_dev_info.triggered.connect(self.show_dev_info)          

           

        global_vars.ui.pushButtonChooseFile.clicked.connect(self.choose_file_thread.on_clicked_choose_file)
        self.choose_file_thread.started.connect(self.choose_file_thread.on_started_choose_file_thread)
        self.choose_file_thread.finished.connect(self.on_finished_choose_file_thread)

        self.choose_sheet_thread.started.connect(self.choose_sheet_thread.on_started)
        self.choose_sheet_thread.finished.connect(self.choose_sheet_thread.on_finished)

        global_vars.ui.checks_started_qty = 0 
        global_vars.ui.checks_results_df = pd.DataFrame()       
     
        global_vars.ui.pushButtonUp.clicked.connect(self.header_up_thread.starter)
        self.header_up_thread.started.connect(self.header_up_thread.on_started)
        self.header_up_thread.finished.connect(self.header_up_thread.on_finished)


        global_vars.ui.pushButtonDown.clicked.connect(header_down)

        #global_vars.ui.pushButtonLoader.clicked.connect(self.load_in_dwh_thread.starter)
        global_vars.ui.pushButtonLoader.clicked.connect(self.load_in_dwh_thread_starter)
        self.load_in_dwh_thread.started.connect(self.load_in_dwh_thread.on_started)
        self.load_in_dwh_thread.finished.connect(self.load_in_dwh_thread.on_finished)

        global_vars.ui.pushButtonLoaderWithTranslit.clicked.connect(self.load_in_dwh_with_translit_headers_thread_starter)
        self.load_in_dwh_with_translit_headers_thread.started.connect(self.load_in_dwh_with_translit_headers_thread.on_started)
        self.load_in_dwh_with_translit_headers_thread.finished.connect(self.load_in_dwh_with_translit_headers_thread.on_finished)
   
        global_vars.header_row = 0

    def show_log_in_dialog(self):
        self.login_dialog_window = LogInDialog(parent = None)
        # self.login_dialog_window.setWindowModality(True)
        self.login_dialog_window.show()

    def show_dev_info(self):
        QtWidgets.QMessageBox.about(None, "Контакты разработчиков", global_vars.dev_info)

    def show_manual(self):
        QtWidgets.QMessageBox.about(None, "Инструкция", global_vars.manual)        
     

####################################################################################
####################################################################################   

    log_in_check_thread = LogInCheck()        # создаём поток проверки подключения 

####################################################################################
#################################################################################### 
  
    load_in_dwh_thread = LoadInDWHThread(translit_headers=False)    # создаём потоки загрузки файла  

    load_in_dwh_with_translit_headers_thread = LoadInDWHThread(translit_headers=True)    # создаём потоки загрузки файла 

####################################################################################
####################################################################################   

    choose_sheet_thread = ChooseSheetThread() # создаём поток загрузки листа

####################################################################################
####################################################################################  

    header_up_thread = HeaderUpThread()       # создаём поток при загрузке файла 

####################################################################################
#################################################################################### 

    choose_file_thread = OpenFileThread()     # создаём поток при загрузке файла   

####################################################################################
####################################################################################       
    
    def on_finished_choose_file_thread(self): # Вызывается при завершении потока
        if global_vars.can_load_file:
            if global_vars.file[-4:] in ['xlsx','.xls']:
                #sheet_names = excel_file_obj.sheet_names 
                #self.comboSheets = QtWidgets.QComboBox()
                #globals.ui.verticalLayoutRight.insertWidget(1, self.comboSheets)

                global_vars.ui.comboSheets.currentIndexChanged.connect(self.choose_sheet_thread.starter) 

                global_vars.ui.comboSheets.clear()
                for sheet_name in  global_vars.sheet_names:
                    global_vars.ui.comboSheets.addItem(sheet_name)                    
                    #self.comboSheets.setFixedWidth(200) 
            else:
                global_vars.ui.comboSheets.setVisible(False)
                fill_in_table() 
                global_vars.ui.footer_label.setStyleSheet('color: green')                
                global_vars.ui.footer_label.setText(f'Файл {global_vars.file} загружен!')


            global_vars.ui.pushButtonUp.setEnabled(True)             
            global_vars.ui.pushButtonDown.setEnabled(True) 
            global_vars.ui.pushButtonLoader.setEnabled(True)  
            global_vars.ui.pushButtonLoaderWithTranslit.setEnabled(True)            
            global_vars.ui.header_label.setStyleSheet('color: black')                
            global_vars.ui.header_label.setText(f'{global_vars.file}')  
        else:
            global_vars.ui.header_label.setStyleSheet('color: red')              
            global_vars.ui.header_label.setText('Выберите файл для загрузки')
            global_vars.ui.footer_label.setStyleSheet('color: red')   
            if global_vars.file:
                global_vars.ui.footer_label.setText(f'Не удалось загрузить {global_vars.file} {global_vars.cant_load_file_reason}') #. Файл должен быть в формате .xls, .xlsx, .xlsm, .xlsb, .ods или .tsv!') 
            else:
                global_vars.ui.footer_label.setText(f'Вы не выбрали файл для загрузки!') #. Файл должен быть в формате .xls, .xlsx, .xlsm, .xlsb, .ods или .tsv!') 


        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)
        global_vars.ui.comboSheets.setEnabled(True) 

    def load_in_dwh_thread_starter(self):
            self.log_in_check_thread.start()
            #print(Fore.MAGENTA, global_vars.log_in_status, Fore.WHITE)
            if global_vars.log_in_status:
                params = get_params()
                if global_vars.file[-4:] in ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']:
                    #sheet_name = globals.ui.comboSheets.currentText()
                    global_vars.dwh_table_name = f'{params[2]}.{params[3]}_LOADED_' + re.sub('\W','_',translit(global_vars.file.split('/')[-1] + '_' + global_vars.sheet_name))
                else:
                    global_vars.dwh_table_name = f'{params[2]}.{params[3]}_LOADED_' + re.sub('\W','_',translit(global_vars.file.split('/')[-1]))
                self.load_in_dwh_thread.start() # Запускаем поток         
            else:
                global_vars.ui.footer_text.setVisible(False) 
                global_vars.ui.footer_label.setStyleSheet('color: red')            
                global_vars.ui.footer_label.setText(f'Не удалось загрузить {global_vars.file}. Проверьте подключение к DWH!') 

    def load_in_dwh_with_translit_headers_thread_starter(self):
            self.log_in_check_thread.start()
            #print(Fore.MAGENTA, global_vars.log_in_status, Fore.WHITE)
            if global_vars.log_in_status:
                params = get_params()
                if global_vars.file[-4:] in ['.xls', 'xlsx', 'xlsm', 'xlsb', '.ods']:
                    #sheet_name = globals.ui.comboSheets.currentText()
                    global_vars.dwh_table_name = f'{params[2]}.{params[3]}_LOADED_' + re.sub('\W','_',translit(global_vars.file.split('/')[-1] + '_' + global_vars.sheet_name))
                else:
                    global_vars.dwh_table_name = f'{params[2]}.{params[3]}_LOADED_' + re.sub('\W','_',translit(global_vars.file.split('/')[-1]))
                self.load_in_dwh_with_translit_headers_thread.start() # Запускаем поток         
            else:
                global_vars.ui.footer_text.setVisible(False) 
                global_vars.ui.footer_label.setStyleSheet('color: red')            
                global_vars.ui.footer_label.setText(f'Не удалось загрузить {global_vars.file}. Проверьте подключение к DWH!')                 

           

################################################################################         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
  
    