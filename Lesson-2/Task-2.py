import json


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        'товар': item,
        'количество': quantity,
        'цена': price,
        'покупатель': buyer,
        'дата': date
    }

    with open('orders.json') as file:
        data = json.loads(file.read())
    data['orders'].append(dict_to_json)

    with open('orders.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


write_order_to_json('Стол', 3, 863, 'Петя', '21.12.2021')
write_order_to_json('Стул', 6, 254, 'Вася', '22.12.2021')
