"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode
и вывести его содержимое.
"""

file = open("test_file.txt", "r")
file.close()
print(file)

#  <_io.TextIOWrapper name='test_file.txt' mode='r' encoding='cp1251'>
#  кодировка файла по умолчанию cp1251

with open('test_file.txt', encoding='utf-8') as file:
    for el_str in file:
        print(el_str, end='')

"""
«сетевое программирование»
«сокет»
«декоратор»
Process finished with exit code 0
"""