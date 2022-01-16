import json
import socket
import sys

from utils import load_configs, send_message, get_message
from log.server_log_config import server_log


CONFIGS = {}


def handle_message(message, CONFIGS):
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        server_log.info('Request received')
        return {CONFIGS.get('RESPONSE'): 200}
    server_log.error('Bad request')
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad request'
    }


def main():
    global CONFIGS
    CONFIGS = load_configs()
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = int(CONFIGS.get('DEFAULT_PORT'))
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        server_log.error('После -\'р\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        server_log.error('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        server_log.error('После -\'а\' необходимо указать адрес для подключения')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(int(CONFIGS.get('MAX_CONNECTIONS')))

    server_log.info('Server ONLINE')

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, CONFIGS)
            response = handle_message(message, CONFIGS)
            send_message(client, response, CONFIGS)
            client.close()
            server_log.info('Принято сообщение от клиента')
        except (ValueError, json.JSONDecodeError):
            server_log.warning('Принято не корректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
