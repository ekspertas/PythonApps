import os
import sys

import logging

sys.path.append('../')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client_logs.log')


client_log = logging.getLogger('client_app')
client_log.setLevel(logging.DEBUG)

my_file_handler = logging.FileHandler(PATH, encoding='cp1251')
file_format = logging.Formatter('%(asctime)s %(levelname)-10s %(module)-7s %(message)s')
my_file_handler.setFormatter(file_format)
my_file_handler.setLevel(logging.DEBUG)

client_log.addHandler(my_file_handler)

if __name__ == '__main__':
    client_log.critical('Критическая ошибка')
    client_log.error('Ошибка')
    client_log.debug('Отладочная информация')
    client_log.info('Информационное сообщение')
