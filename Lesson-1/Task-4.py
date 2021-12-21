"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

worlds = ['разработка', 'администрирование', 'protocol', 'standard']
worlds_in_bytes = []

for world in worlds:
    world_in_bytes = world.encode("utf-8")
    worlds_in_bytes.append(world_in_bytes)
    print(f'Слово "{world}" в байтовом представлении {world_in_bytes}')

for world in worlds_in_bytes:
    print(f'{world} - байтовое представление слова "{world.decode("utf-8")}"')
