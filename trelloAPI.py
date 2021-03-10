import sys
import requests

# Добавьте рядом с названием колонки цифру, отражающую количество задач в ней.
# Реализуйте создание колонок.
# Обработайте совпадающие имена задач *
# Как вы думаете, что случится, если у нас появится две задачи с одинаковым именем? Реализуйте обработку такой ситуации.
# Пользователь должен иметь возможность управлять всеми задачами вне зависимости от того, как он их называет.
#
# Сейчас при работе с задачей мы перебираем все задачи и работаем с первой найденной по имени. Нужно проверять,
# имеются ли еще задачи с таким именем и выводить их в консоль. Помимо имени должны быть указаны: колонка, в которой
# находится эта задача, и другие параметры, по которым можно было бы отличить одну задачу от другой. Пользователю должно
# быть предложено дополнительно ввести (при помощи функции input) номер для выбора задачи из полученного списка. Наш
# клиент должен работать с выбранной задачей.

# Данные авторизации в API Trello
auth_params = {
    'key': 'f8007a1d55f72d118672587e98b4fdb0',
    'token': '27bb7c00efab9230b8112d69b2536ac7d31d60d099bfca1541f3dcfd197370f6',
}

# Адрес, на котором расположен API Trello, именно туда мы будем отправлять HTTP запросы.
base_url = 'https://api.trello.com/1/{}'
board_id = 'CWN230ZH'


def read_and_update():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        column['length'] = len(task_data)
        temp_list = list(column['name'])
        temp_list.insert(0, f"{column['length']}")
        column['name'] = ''.join(temp_list)

        requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column['name'], **auth_params})
        print('column: ', column)
        # column: {'id': '60410d46c0141d8a5b6dad5a', 'name': 'Нужно сделать', 'closed': False, 'pos': 16384,
        #          'softLimit': None, 'idBoard': '60410d46c0141d8a5b6dad59', 'subscribed': False}p
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        print(len(task_data))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('task: ', task)
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    print('column_data: ', column_data)
    # column_data: [
    #     {'id': '60410d46c0141d8a5b6dad5a', 'name': 'Нужно сделать', 'closed': False, 'pos': 16384, 'softLimit': None,
    #      'idBoard': '60410d46c0141d8a5b6dad59', 'subscribed': False},
    #     {'id': '60410d46c0141d8a5b6dad5b', 'name': 'В процессе', 'closed': False, 'pos': 32768, 'softLimit': None,
    #      'idBoard': '60410d46c0141d8a5b6dad59', 'subscribed': False},
    #     {'id': '60410d46c0141d8a5b6dad5c', 'name': 'Готово', 'closed': False, 'pos': 49152, 'softLimit': None,
    #      'idBoard': '60410d46c0141d8a5b6dad59', 'subscribed': False}]

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def create_column(column_name):
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read_and_update()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])

