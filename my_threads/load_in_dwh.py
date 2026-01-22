from PySide6 import QtCore, QtWidgets
from colorama import Fore
from my_functions.preprocessing import preprocessing
from my_functions.dwh import execute_sql_click, insert_from_df
from my_functions.main_window import translit, load_file_sheet_name
import global_vars
import pandas as pd
import re
import pyperclip

class LoadInDWHThread(QtCore.QThread):



    def __init__ (self, translit_headers, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.translit_headers = translit_headers

    def run(self):
        load_file_sheet_name()
        global_vars.ui.footer_label.setStyleSheet('color: blue')
        global_vars.ui.footer_label.setText(f"Подготавливаем данные к загрузке в DWH...") 

        if self.translit_headers:
            global_vars.horizontal_headers = [translit(header) for header in global_vars.horizontal_headers]
            print(global_vars.horizontal_headers)  
            rows_number_column_name = 'Stroka_v_ishodnike'
        else:
            rows_number_column_name = 'Строка в исходнике'            
   
            

        df_to_Insert = preprocessing(global_vars.df, global_vars.header_row, global_vars.horizontal_headers, global_vars.column_formats, rows_number_column_name)

        #df_to_Insert = df_to_Insert.map(str)
        #print(df_to_Insert)
        #globals.ui.statusbar.showMessage(dwh_table_name)
        tableColumnList = [f'`{rows_number_column_name}` Int32']

        

        for column_name, column_format in zip(global_vars.horizontal_headers, global_vars.column_formats ):

            if 'Null' in column_format.currentText() or 'NaN' in column_format.currentText():
                tableColumnList.append(f"`{column_name}` {column_format.currentText().replace('NaN', 'Null')} Null")
            else:
                if column_format.currentText() in ['Vagon','Container']:
                    tableColumnList.append(f"`{column_name}` String") 
                else:    
                    tableColumnList.append(f"`{column_name}` {column_format.currentText()}")                


        tableColumnStr = f',\n'.join(tableColumnList)
        global_vars.ui.footer_label.setStyleSheet('color: blue')        
        global_vars.ui.footer_label.setText(f"Создаём таблицу {global_vars.dwh_table_name} в DWH...") 

        try:   
            sql = f'''
            CREATE OR REPLACE TABLE {global_vars.dwh_table_name}
            (\n{tableColumnStr})
            ENGINE = MergeTree()
            ORDER BY `{rows_number_column_name}`
            '''.replace(f'`{rows_number_column_name}` String',f'`{rows_number_column_name}` Int32').replace('OrNull','')  

            #print(sql)
            #pyperclip.copy(sql)
            #input('aaaaaaaaaaaaaaaaa')

            # sql = f'''
            # CREATE OR REPLACE TABLE {global_vars.dwh_table_name}
            # (\n{tableColumnStr})
            # ENGINE = MergeTree()
            # ORDER BY `Строка в исходнике`
            # '''.replace('`Строка в исходнике` String','`Строка в исходнике` Int32').replace('OrNull','')  



            execute_sql_click(sql, operation_name = 'Создаём таблицу в базе данных')

            global_vars.ui.footer_label.setStyleSheet('color: blue')            
            global_vars.ui.footer_label.setText(f"Загружаем в таблицу {global_vars.dwh_table_name} данные из файла...")   
            insert_from_df(global_vars.dwh_table_name,
                           df_to_Insert,
                           operation_name = f'Загружаем данные в таблицу {global_vars.dwh_table_name}')

            self.engine = 'MergeTree()' 
        except:

            print('Внимание: таблица будет создана с движком Memory()!')
            sql = f'''
            CREATE OR REPLACE TABLE {global_vars.dwh_table_name}
            (\n{tableColumnStr})
            ENGINE = Memory()
            '''.replace('`Строка в исходнике` String','`Строка в исходнике` Int32').replace('OrNull','')  

            #print(sql)

            execute_sql_click(sql, operation_name = 'Создаём таблицу в базе данных')
            #input('Пауза')
            global_vars.ui.footer_label.setStyleSheet('color: blue')            
            global_vars.ui.footer_label.setText(f"Загружаем в таблицу {global_vars.dwh_table_name} данные из файла...")   
            insert_from_df(global_vars.dwh_table_name, df_to_Insert, operation_name = f'Загружаем данные в таблицу {global_vars.dwh_table_name}')

            self.engine = 'Memory()'           


    def on_started(self): # Вызывается при запуске потока
        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
        global_vars.ui.comboSheets.setEnabled(False) 
        global_vars.ui.footer_text.setVisible(False)          
        


    def on_finished(self): # Вызывается при завершении потока
        global_vars.ui.verticalLayoutWidgetButtons.setEnabled(True)
        global_vars.ui.comboSheets.setEnabled(True) 
        if self.engine == 'Memory()':
            global_vars.ui.footer_label.setStyleSheet('color: red')
            global_vars.ui.footer_label.setText(f"Внимание: файл загружен в таблицу с движком {self.engine}!")            
        else:  
            global_vars.ui.footer_label.setStyleSheet('color: green')             
            global_vars.ui.footer_label.setText(f"Файл загружен в таблицу (название уже в буфере обмена):")
        global_vars.ui.footer_text.setVisible(True)
        pyperclip.copy(global_vars.dwh_table_name)
        global_vars.ui.footer_text.setText(global_vars.dwh_table_name)
