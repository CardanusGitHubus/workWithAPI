import sys
import requests

import auth_params

# Данные авторизации в API Trello
auth_params = {
    'key': auth_params.KEY,
    'token': auth_params.TOKEN,
}

# Адрес, на котором расположен API Trello, именно туда мы будем отправлять HTTP запросы.
base_url = 'https://api.trello.com/1/{}'
board_id = '60410d46c0141d8a5b6dad59'


def is_list_exist(list_name):
    list_id = None
    list_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for list in list_data:
        if list['name'] == list_name:
            list_id = list['id']
            return list_id


def read():
    # Получим данные всех колонок на доске:
    list_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Выведем название каждой колонки и всех заданий, которые к ней относятся
    # и обновим информацию о количестве задач в каждой из колонок:
    for list in list_data:
        card_data = requests.get(base_url.format('lists') + '/' + list['id'] + '/cards', params=auth_params).json()
        # Добавьте рядом с названием колонки цифру, отражающую количество задач в ней. -------------DONE
        print(list['name'], '| Задач:', len(card_data))

        # Получим данные всех задач в колонке и перечислим все названия
        if not card_data:
            print('\t' + 'Нет задач!')
            continue
        for card in card_data:
            print('\t' + card['name'])


def create_card(name, list_name):
    # Проверим, существует ли колонка с таким именем
    list_id = is_list_exist(list_name)

    # Если нет - создадим ее
    if list_id is None:
        list_id = create_list(list_name)['id']

    # Добавим задачу в колонку
    requests.post(base_url.format('cards'), data={'name': name, 'idList': list_id, **auth_params})


# Реализуйте создание колонок. -------------DONE
def create_list(list_name):
    return requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': list_name,
                                                                                      **auth_params}).json()


def move_card(name, list_name):
    # Обработайте совпадающие имена задач -------------DONE
    # Получим данные всех колонок на доске
    list_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок ищем все задачи с введенным именем и добавляем в список их id, имя задачи и имя колонки
    cards = []
    card_id = None
    for list in list_data:
        list_cards = requests.get(base_url.format('lists') + '/' + list['id'] + '/cards', params=auth_params).json()
        for card in list_cards:
            if card['name'] == name:
                cards.append([card['id'], card['name'], list['name']])
    # Различное поведение функции при нахождении одной задачи, нескольких задач, или при отсутствии искомой задачи
    if len(cards) == 0:
        print('Ошибка: такой задачи нет')
    elif len(cards) == 1:
        card_id = cards[0][0]
    else:
        print(f'Найдено {len(cards)} задач. Введите номер задачи для перемещения:')
        for idx, card in enumerate(cards):
            print('\t' + str(idx + 1) + '. ' + card[1] + ' | Колонка: ', card[2])
        card_idx = int(input())
        card_id = cards[card_idx - 1][0]

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Получим ID колонки, в которую мы будем перемещать задачу
    list_id = is_list_exist(list_name)
    if list_id is None:
        list_id = create_list(list_name)['id']

    # Выполним запрос к API для перемещения задачи в нужную колонку
    requests.put(base_url.format('cards') + '/' + card_id + '/idList', data={'value': list_id, **auth_params})


def delete_card(name):
    # Логика функции подобна функции move_card
    list_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    cards = []
    card_id = None
    for list in list_data:
        list_cards = requests.get(base_url.format('lists') + '/' + list['id'] + '/cards', params=auth_params).json()
        for card in list_cards:
            if card['name'] == name:
                cards.append([card['id'], card['name'], list['name']])
    if len(cards) == 0:
        print('Ошибка: такой задачи нет')
    elif len(cards) == 1:
        card_id = cards[0][0]
    else:
        print(f'Найдено {len(cards)} задач. Введите номер задачи для удаления:')
        for idx, card in enumerate(cards):
            print('\t' + str(idx + 1) + '. ' + card[1] + ' | Колонка: ', card[2])
        card_idx = int(input())
        card_id = cards[card_idx - 1][0]
        print('card_id', card_id)

    requests.delete(base_url.format('cards') + '/' + card_id, params=auth_params)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create_card':
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move_card':
        move_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_list':
        create_list(sys.argv[2])
    elif sys.argv[1] == 'delete_card':
        delete_card(sys.argv[2])

