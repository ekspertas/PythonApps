import argparse
import json
import socket
import sys
import select
import time

from utils import load_configs, send_message, get_message, log
from log.server_log_config import server_log

CONFIGS = {}


@log
def handle_message(message, messages_list, client, CONFIGS):
    server_log.debug(f'Обработка сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        send_message(client, {CONFIGS.get('RESPONSE'): 200}, CONFIGS)
        # return
        return {CONFIGS.get('RESPONSE'): 200}
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS['MESSAGE'] \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('MESSAGE_TEXT') in message:
        messages_list.append((message[CONFIGS.get('ACCOUNT_NAME')], message[CONFIGS.get('MESSAGE_TEXT')]))
        return
    # Иначе отдаём Bad request
    server_log.error('Bad request')
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad request'
    }


def arg_parser(CONFIGS):
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 2 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверим подходящий номер порта
    if not 1023 < listen_port < 65536:
        server_log.critical(f'Попытка запуска сервера с некорректного порта {listen_port}.'
                            'Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    return listen_address, listen_port


def main():
    global CONFIGS
    CONFIGS = load_configs()
    """Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию"""
    listen_address, listen_port = arg_parser(CONFIGS)
    server_log.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(int(CONFIGS.get('MAX_CONNECTIONS')))
    server_log.info('Server ONLINE')

    # Основной цикл программы сервера
    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            server_log.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    handle_message(get_message(client_with_message, CONFIGS), messages, client_with_message, CONFIGS)
                    c = handle_message(get_message(client_with_message, CONFIGS), messages, client_with_message, CONFIGS)
                    print(c)
                    print(8)
                except:
                    server_log.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                CONFIGS['ACTION']: CONFIGS['MESSAGE'],
                CONFIGS['SENDER']: messages[0][0],
                CONFIGS['TIME']: time.time(),
                CONFIGS['MESSAGE_TEXT']: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message, CONFIGS)
                except:
                    server_log.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)

    # while True:
    #     client, client_address = transport.accept()
    #     try:
    #         message = get_message(client, CONFIGS)
    #         response = handle_message(message, CONFIGS)
    #         send_message(client, response, CONFIGS)
    #         client.close()
    #         server_log.info('Принято сообщение от клиента')
    #     except (ValueError, json.JSONDecodeError):
    #         server_log.warning('Принято не корректное сообщение от клиента')
    #         client.close()


if __name__ == '__main__':
    main()
