import os
import sys

import logging
from logging import handlers

sys.path.append('../')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server_logs.log')

server_log = logging.getLogger('server_app')
server_log.setLevel(logging.DEBUG)

my_file_handler = logging.FileHandler(PATH, encoding='cp1251')
file_format = logging.Formatter('%(asctime)s %(levelname)-10s %(module)-7s %(message)s')
my_file_handler.setFormatter(file_format)
my_file_handler.setLevel(logging.DEBUG)
handlers.TimedRotatingFileHandler(PATH, encoding='cp1251', interval=1, when='D')

server_log.addHandler(my_file_handler)

if __name__ == '__main__':
    server_log.critical('Критическая ошибка')
    server_log.error('Ошибка')
    server_log.debug('Отладочная информация')
    server_log.info('Информационное сообщение')
