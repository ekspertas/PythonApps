"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

word_1 = b'class'
word_2 = b'function'
word_3 = b'method'

print(word_1, type(word_1), len(word_1))  # b'class' <class 'bytes'> 5
print(word_2, type(word_2), len(word_2))  # b'function' <class 'bytes'> 8
print(word_3, type(word_3), len(word_3))  # b'method' <class 'bytes'> 6
