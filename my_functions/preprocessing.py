'''
Модуль содержит фунции, которые преобразают данные в таблице в соответствии с нужным форматом
'''

from colorama import Fore
from pandas import DataFrame
from PySide6 import QtWidgets
from re import sub
import time 
import global_vars

def parse(date_str):
        patterns = ['%d-%m-%Y %H:%M:%S',
                    '%d-%m-%Y %H:%M',
                    '%d-%m-%Y',
                    '%d.%m.%Y %H:%M:%S',
                    '%d.%m.%Y %H:%M',
                    '%d.%m.%Y'
                    '%d.%m.%Y %H:%M:%S',
                    '%d.%m.%Y %H:%M',
                    '%d.%m.%Y',
                    '%Y-%m-%d %H:%M:%S.%f',                    
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%Y-%m-%d',
                    '%Y.%m.%d %H:%M:%S',                    
                    '%Y.%m.%d'               
                    ]
                    
        for pattern in patterns:
            try:
                dt = time.strptime(date_str, pattern)
                result = f"{dt.tm_year}-{str(dt.tm_mon).zfill(2)}-{str(dt.tm_mday).zfill(2)} {str(dt.tm_hour).zfill(2)}:{str(dt.tm_min).zfill(2)}:{str(dt.tm_sec).zfill(2)}"
                return result
            except:
                pass
        raise ValueError (f"Значяение {date_str} не соответствует ни одному паттерну даты!")


def preprocessing(df, header_row, column_names, column_formats, rows_number_column_name):
    preprocessing_dict = {'Date'          : DateTimeOrNull,
                          'DateOrNull'    : DateTimeOrNull,
                          'DateTime'      : DateTimeOrNull,
                          'DateTimeOrNull': DateTimeOrNull,
                          'Int32'         : Int32OrNull,
                          'Int32OrNull'    : Int32OrNull,
                          'Float32'       : Float32OrNaN,
                          'Float32OrNaN'  : Float32OrNaN
                          }

    df_to_Insert         = df.reset_index(names = rows_number_column_name)
    df_to_Insert         = df_to_Insert.iloc[header_row:]
    df_to_Insert.columns = [rows_number_column_name] + column_names
    df_to_Insert.columns = map(str, df_to_Insert.columns)
    df_to_Insert         = df_to_Insert.map(str)

    i=0
    for column_name, column_format in zip(column_names, column_formats):
        i += 1
        global_vars.ui.footer_label.setText(f"Подготавливаем к загрузке столбец {i} из {len(column_names)}: {column_name}")
        time.sleep(0.1)
        if preprocessing_dict.get(column_format.currentText()) is not None:
            #print(Fore.YELLOW,preprocessing_dict.get(column_format.currentText())(df_to_Insert[column_name]))
            df_to_Insert[column_name] = preprocessing_dict.get(column_format.currentText())(df_to_Insert[column_name])
        
    #(Fore.YELLOW, df_to_Insert)
    return df_to_Insert


def DateTimeOrNull(column_values):
    values_to_preprocess = map(str, column_values)
    #values_to_preprocess = list(map(sub, values_to_preprocess))    
    values_to_download = []    
    for value in values_to_preprocess:
        try:
            values_to_download.append(parse(value))
        except:
            values_to_download.append(None)
    return values_to_download


def Int32OrNull(column_values):
    values_to_preprocess = map(str, column_values)
    #values_to_preprocess = list(map(sub, values_to_preprocess))  
    values_to_download = []    
    for value in values_to_preprocess:
        try:
            values_to_download.append(int(float(value.replace(' ','').replace(',','.').replace(chr(160),''))))
        except:
            values_to_download.append(None)
    return values_to_download


def Float32OrNaN(column_values):
    values_to_preprocess = map(str, column_values)
    #values_to_preprocess = list(map(sub, values_to_preprocess)) 
    
    values_to_download = []    
    for value in values_to_preprocess:
        try:
            values_to_download.append(float(value.replace(' ','').replace(',','.').replace(chr(160),'')))
        except:
            values_to_download.append(None)
    return values_to_download