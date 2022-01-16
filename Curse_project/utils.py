import json
import os
import sys
from dotenv import load_dotenv


def load_configs(is_server=True):
    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'PRESENCE',
        'RESPONSE',
        'ERROR'
    ]
    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')

    CONFIGS= {}
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        for key in config_keys:
            CONFIGS[key] = os.getenv(key)
            if os.getenv(key) is None:
                print(f'В файле конфигурации не хватает ключа: {key}')
                sys.exit(1)
    else:
        print('Файл конфигурации не найден')
        sys.exit(1)

    return CONFIGS


def send_message(opened_socket, message, CONFIGS):
    json_message = json.dumps(message)
    response = json_message.encode(CONFIGS.get('ENCODING'))
    opened_socket.send(response)


def get_message(opened_socket, CONFIGS):
    response = opened_socket.recv(int(CONFIGS.get('MAX_PACKAGE_LENGTH')))
    if isinstance(response, bytes):
        json_response = response.decode(CONFIGS.get('ENCODING'))
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError
