import yaml


data_to_yaml = {
    'key-1': ['val1', 'val2', 3],
    'key-2': 777,
    'key-3': {
        'inner_key-1': '858€',  # символы '€', '‡' есть в сводной таблице кодов ASCII
        'inner_key-2': '3‡',    # https://www.calc.ru/Tablitsa-Kodov-Ascii.html
        'inner_key-3': 'Ð584',
        'inner_key-4': '3È',    # символов 'Ð', 'È' нет в сводной таблице кодов ASCII
    }
}

with open('data_write.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data_to_yaml, file, default_flow_style=False, allow_unicode=True)

with open('data_write.yaml', encoding='utf-8') as file:
    print(file.read())
