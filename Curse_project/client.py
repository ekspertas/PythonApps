import json
import sys
import socket
import time
import argparse

from utils import load_configs, send_message, get_message, log
from log.client_log_config import client_log
from log.server_log_config import server_log
from errors import ReqFieldMissingError, ServerError

CONFIGS = {}


@log
def create_presence_message(CONFIGS, account_name='Guest'):
    """Функция генерирует запрос о присутствии клиента"""
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    client_log.info('Пользователь в сети')
    return message


def get_user_message(sock, CONFIGS, account_name='Guest'):
    """ Функция запрашивает текст сообщения и возвращает его.
        Так же завершает работу при вводе комманды '!!!' """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        client_log.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        CONFIGS['ACTION']: 'message',
        CONFIGS['MESSAGE']: 'message',
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['MESSAGE_TEXT']: message
    }
    client_log.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


def handle_server_message(message, CONFIG):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if CONFIG['ACTION'] in message and message[CONFIG['ACTION']] == CONFIG['MESSAGE'] and \
            CONFIG['SENDER'] in message and CONFIG['MESSAGE_TEXT'] in message:
        print(f'Получено сообщение от пользователя '
              f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
        server_log.info(f'Получено сообщение от пользователя '
                        f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
    else:
        client_log.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def handle_response(message, CONFIGS):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    """
    print(message)
    print('6')
    client_log.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            client_log.info('Успешный запрос')
            return '200 : OK'
        client_log.error('Ошибочный запрос')
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


@log
def arg_parser(CONFIGS):
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    print(parser)
    parser.add_argument('addr', default=CONFIGS['DEFAULT_IP_ADDRESS'], nargs='?')
    parser.add_argument('port', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        client_log.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        server_log.critical(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    """Загружаем параметы коммандной строки"""
    server_address, server_port, client_mode = arg_parser(CONFIGS)

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        print('1')
        send_message(transport, create_presence_message(CONFIGS), CONFIGS)
        print('2')
        b = get_message(transport, CONFIGS)
        print(b)
        print(10)
        answer = handle_response(b, CONFIGS)
        print(client_mode)
        client_log.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        client_log.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        client_log.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        client_log.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        client_log.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')

        while True:
            # режим работы - отправка сообщений
            print(client_mode)
            if client_mode == 'send':
                try:
                    send_message(transport, get_user_message(transport, CONFIGS), CONFIGS)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    handle_server_message(get_message(transport, CONFIGS), CONFIGS)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


# def main():
#     global CONFIGS
#     CONFIGS = load_configs(is_server=False)
#     try:
#         server_address = sys.argv[1]
#         print(server_address)
#         server_port = int(sys.argv[2])
#         if not 65535 >= server_port >= 1024:
#             raise ValueError
#     except ValueError:
#         client_log.error('Порт должен быть указан в пределах от 1024 до 65535')
#         sys.exit(1)
#     except IndexError:
#         client_log.info('IP адрес и порт установлены "по умолчанию"')
#         server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
#         server_port = int(CONFIGS.get('DEFAULT_PORT'))
#
#     transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     transport.connect((server_address, server_port))
#     presence_message = create_presence_message(CONFIGS, 'Guest')
#     client_log.info('Отправка сообщения на сервер')
#     send_message(transport, presence_message, CONFIGS)
#     try:
#         response = get_message(transport, CONFIGS)
#         handled_response = handle_response(response, CONFIGS)
#         client_log.info(f'Ответ от сервера: {response}')
#         client_log.info(f'Обработанный ответ сервера: {handled_response}')
#     except (ValueError, json.JSONDecodeError):
#         client_log.error('Ошибка декодирования сообщения')


if __name__ == '__main__':
    main()
