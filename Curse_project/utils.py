import os
import sys
# from dotenv import load_dotenv


def load_config(is_server=True):
    config_keys = [
        'DEFAULT_IP_ADDRESS',
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
    if not os.path.exists('.env'):
        print('Файл конфигурации не найден')
        sys.exit(1)

    CONFIGS= {}
    # load_dotenv(dotenv_path=os.path)
    for key in config_keys:
        CONFIGS[key] = os.getenv(key)

    return CONFIGS


a = load_config()
print(a)
b = os.getenv('ERROR')
print(b)
