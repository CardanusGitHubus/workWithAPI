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
board_id = 'CWN230ZH'


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    column_tasks = {}

    # Выведем название каждой колонки и всех заданий, которые к ней относятся
    # и обновим информацию о количестве задач в каждой из колонок:
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        column_tasks[column['name']] = len(task_data)

        # Добавьте рядом с названием колонки цифру, отражающую количество задач в ней. -------------DONE

        print(column['name'], '| Задач:', column_tasks[column['name']])

        # Получим данные всех задач в колонке и перечислим все названия

        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create_card(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    print('column_data: ', column_data)

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


# Реализуйте создание колонок. -------------DONE
def create_list(column_name):
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})


def move_card(name, column_name):
    # Обработайте совпадающие имена задач -------------DONE
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    print('column data:', column_data)

    # Среди всех колонок ищем все задачи с введенным именем и добавляем в список их id, имя задачи и имя колонки
    tasks = []
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print('column_tasks', column_tasks)
        for task in column_tasks:
            if task['name'] == name:
                tasks.append([task['id'], task['name'], column['name']])
    print('tasks', tasks)
    # Различное поведение функции при нахождении одной задачи, нескольких задач, или при отсутствии искомой задачи
    if len(tasks) == 0:
        print('Ошибка: такой задачи нет')
    elif len(tasks) == 1:
        task_id = tasks[0][0]
    else:
        print(f'Найдено {len(tasks)} задач. Введите номер задачи для перемещения:')
        for idx, task in enumerate(tasks):
            print('\t' + str(idx + 1) + '. ' + task[1] + ' | Колонка: ', task[2])
        task_idx = int(input())
        task_id = tasks[task_idx - 1][0]
        print('task_id', task_id)

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break


def delete_card(name):
    # Логика функции подобна функции move_card
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    tasks = []
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print('column_tasks', column_tasks)
        for task in column_tasks:
            if task['name'] == name:
                tasks.append([task['id'], task['name'], column['name']])
    print('tasks', tasks)
    if len(tasks) == 0:
        print('Ошибка: такой задачи нет')
    elif len(tasks) == 1:
        task_id = tasks[0][0]
    else:
        print(f'Найдено {len(tasks)} задач. Введите номер задачи для удаления:')
        for idx, task in enumerate(tasks):
            print('\t' + str(idx + 1) + '. ' + task[1] + ' | Колонка: ', task[2])
        task_idx = int(input())
        task_id = tasks[task_idx - 1][0]
        print('task_id', task_id)

    requests.delete(base_url.format('cards') + '/' + task_id, params=auth_params)


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

