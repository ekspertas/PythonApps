import re
import csv


csv_file_link = 'main_data.csv'
file_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
param_list = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def get_data(files, params):
    main_data = []
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    pattern = '.*:\s+([^:\n]+)+'
    for file in files:
        with open(file, 'r', encoding='cp1251') as source_file:
            for line in source_file.readlines():
                if re.search(params[0], line):
                    os_prod_list += re.findall(pattern, line)
                if re.search(params[1], line):
                    os_name_list += re.findall(pattern, line)
                if re.search(params[2], line):
                    os_code_list += re.findall(pattern, line)
                if re.search(params[3], line):
                    os_type_list += re.findall(pattern, line)
    main_data += params, os_prod_list, os_name_list, os_code_list, os_type_list
    return main_data


def write_to_csv(file_link, files, params):
    data = get_data(files, params)
    with open(file_link, 'w', newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerows(data)

"""
Без параметра newline='' файл csv формируется в виде:
Изготовитель системы,Название ОС,Код продукта,Тип системы

LENOVO,ACER,DELL

и т.д.
"""
write_to_csv(csv_file_link, file_list, param_list)

with open('main_data.csv') as file:
    file_reader = csv.reader(file)
    file_headers = next(file_reader)
    print('Headers: ', file_headers)
    for row in file_reader:
        print(row)

"""
Данные выводятся в виде списков:
Headers:  ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
['LENOVO', 'ACER', 'DELL']
и т.д.

На уроке выводилось просто в виде строк.
Возможно это из-за Windows 10, хотя я пытался менять кодировки чтения и записи.
Мне так и не удалось разобраться, в чем причина.
"""
