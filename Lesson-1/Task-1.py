"""
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
и проверить тип и содержание соответствующих переменных. Затем с помощью онлайн-конвертера
преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.
"""

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'

print(word_1, type(word_1))  # > разработка <class 'str'>

print(word_2, type(word_2))  # > сокет <class 'str'>

print(word_3, type(word_3))  # > декоратор <class 'str'>

word_1_unicode = '\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430'
print(word_1_unicode, type(word_1_unicode))  # > разработка <class 'str'>

word_2_unicode = '\u0441\u043E\u043A\u0435\u0442'
print(word_2_unicode, type(word_2_unicode))  # > сокет <class 'str'>

word_3_unicode = '\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440'
print(word_3_unicode, type(word_3_unicode))  # > декоратор <class 'str'>
