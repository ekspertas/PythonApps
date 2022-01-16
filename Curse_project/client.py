import json
import sys
import socket
import time


from utils import load_configs, send_message, get_message
from log.client_log_config import client_log

CONFIGS = {}


def create_presence_message(account_name, CONFIGS):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    client_log.info('Пользователь в сети')
    return message


def handle_response(message, CONFIGS):
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            client_log.info('Успешный запрос')
            return '200 : OK'
        client_log.error('Ошибочный запрос')
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except ValueError:
        client_log.error('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)
    except IndexError:
        client_log.info('IP адрес и порт установлены "по умолчанию"')
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = int(CONFIGS.get('DEFAULT_PORT'))

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = create_presence_message('Guest', CONFIGS)
    client_log.info('Отправка сообщения на сервер')
    send_message(transport, presence_message, CONFIGS)
    try:
        response = get_message(transport, CONFIGS)
        handled_response = handle_response(response, CONFIGS)
        client_log.info(f'Ответ от сервера: {response}')
        client_log.info(f'Обработанный ответ сервера: {handled_response}')
    except (ValueError, json.JSONDecodeError):
        client_log.error('Ошибка декодирования сообщения')


if __name__ == '__main__':
    main()
