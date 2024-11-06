import global_vars
import pandas as pd
import re
from PySide6 import QtCore
from colorama import Fore
from my_functions.preprocessing import parse
from time import sleep

no_errs_df = pd.DataFrame(columns = ['column_number','Сообщение','Ячейка LN','Ячейка RNCN','Значение'])



def columnNumberToLetters(number):
    """
    Функция преобразует номер столбца в буквенное обозначение как в Excel
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWYXZ"
    output = ""
    while(number):
        output = letters[(number - 1) % 26] + output
        number = number // 26
    return output    



def check_String(column_values, column_number, header_row, mysignal):
    print('check_String')
    sleep(0.1)
    return (no_errs_df, "background-color: none")
def check_DateTimeOrNull(column_values, column_number, header_row, mysignal): 
    print('check_DateTimeOrNull')
    sleep(0.1)        
    return (no_errs_df, "background-color: blue")
def check_DateOrNull(column_values, column_number, header_row, mysignal):  
    print('check_DateOrNull')   
    sleep(0.1)     
    return (no_errs_df, "background-color: blue")
def check_Int32OrNull(column_values, column_number, header_row, mysignal):   
    print('check_Int32OrNull')
    sleep(0.1)          
    return (no_errs_df, "background-color: blue")
def check_Float32OrNaN(column_values, column_number, header_row, mysignal):    
    print('check_Float32OrNul')  
    sleep(0.1)          
    return (no_errs_df, "background-color: blue")
    
def check_DateTime(column_values, column_number, header_row, mysignal):
    print('check_DateTime')
    global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
    global_vars.ui.comboSheets.setEnabled(False)         
    err_list = []
    values_to_check = list(map(str, column_values[header_row:]))
    row_number = 1
    for value in values_to_check:#, total=len(column):
        try:
            parse(value)
        except:
            err_list.append({'column_number' : column_number,
                                'Сообщение'     : 'DateTime',
                                'Ячейка LN'     : f'{columnNumberToLetters(column_number+1)}{row_number + header_row}',
                                'Ячейка RNCN'   : f'R{row_number + header_row}C{column_number+1}',
                                'Значение'      : str(value)
                                })
        
        mysignal.emit(('checks', column_number, len(values_to_check), row_number))
        row_number += 1
    if err_list == []:
        return (no_errs_df, "background-color: green")
    else:
        return (pd.DataFrame(err_list), "background-color: red")



def check_Int32(column_values, column_number, header_row, mysignal):
    print('check_Int32')
    global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
    global_vars.ui.comboSheets.setEnabled(False)      
    err_list = []
    values_to_check = list(map(str, column_values[header_row:]))
    row_number = 1
    for value in values_to_check:#, total=len(column):
        try:
            int(float(value.replace(' ','').replace(',','.').replace(chr(160),'')))
        except:
            err_list.append({'column_number' : column_number,
                                'Сообщение'     : 'Int32',
                                'Ячейка LN'     : f'{columnNumberToLetters(column_number+1)}{row_number + header_row}',
                                'Ячейка RNCN'   : f'R{row_number + header_row}C{column_number+1}',
                                'Значение'      : str(value)
                                })
        sleep(0.00000001)            
        mysignal.emit(('checks', column_number, len(values_to_check), row_number))                
        row_number += 1

    if err_list == []:
        return (no_errs_df, "background-color: green")
    else:
        return (pd.DataFrame(err_list), "background-color: red")
    

def check_Float32(column_values, column_number, header_row, mysignal):
    print('check_Float32')
    global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
    global_vars.ui.comboSheets.setEnabled(False)                
    err_list = []
    values_to_check = list(map(str, column_values[header_row:]))
    row_number = 1
    for value in values_to_check:#, total=len(column):
        try:
            float(value.replace(' ','').replace(',','.').replace(chr(160),''))
        except:
            err_list.append({'column_number' : column_number,
                                'Сообщение'     : 'Float32',
                                'Ячейка LN'     : f'{columnNumberToLetters(column_number+1)}{row_number + header_row}',
                                'Ячейка RNCN'   : f'R{row_number + header_row}C{column_number+1}',
                                'Значение'      : str(value)
                                })
        sleep(0.00000001)            
        mysignal.emit(('checks', column_number, len(values_to_check), row_number))        
        row_number += 1
    if err_list == []:
        return (no_errs_df, "background-color: green")
    else:
        return (pd.DataFrame(err_list), "background-color: red")


def check_Container(column_values, column_number, header_row, mysignal):
    print('check_Container')
    pattern = re.compile(r'[A-Z]{4}\d{7}')
    global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
    global_vars.ui.comboSheets.setEnabled(False)         
    err_list = []
    values_to_check = list(map(str, column_values[header_row:]))
    row_number = 1
    for value in values_to_check:#, total=len(column):
        if len(value) != 11 or re.match(pattern, value) is None:
            err_list.append({'column_number' : column_number,
                                'Сообщение'     : 'ContainerNumber',
                                'Ячейка LN'     : f'{columnNumberToLetters(column_number+1)}{row_number + header_row}',
                                'Ячейка RNCN'   : f'R{row_number + header_row}C{column_number+1}',
                                'Значение'      : str(value)
                                })
        
        mysignal.emit(('checks', column_number, len(values_to_check), row_number))
        row_number += 1
    if err_list == []:
        return (no_errs_df, "background-color: green")
    else:
        return (pd.DataFrame(err_list), "background-color: red")
    

def check_Vagon(column_values, column_number, header_row, mysignal):
    print('check_Vagon')
    pattern = re.compile(r'\d{8}')
    global_vars.ui.verticalLayoutWidgetButtons.setEnabled(False)
    global_vars.ui.comboSheets.setEnabled(False)         
    err_list = []
    values_to_check = list(map(str, column_values[header_row:]))
    row_number = 1
    for value in values_to_check:#, total=len(column):
        if len(value) != 8 or re.match(pattern, value) is None:
            err_list.append({'column_number' : column_number,
                                'Сообщение'     : 'VagonNumber',
                                'Ячейка LN'     : f'{columnNumberToLetters(column_number+1)}{row_number + header_row}',
                                'Ячейка RNCN'   : f'R{row_number + header_row}C{column_number+1}',
                                'Значение'      : str(value)
                                })
        
        mysignal.emit(('checks', column_number, len(values_to_check), row_number))
        row_number += 1
    if err_list == []:
        return (no_errs_df, "background-color: green")
    else:
        return (pd.DataFrame(err_list), "background-color: red")    
