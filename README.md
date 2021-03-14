# workWithAPI
This is my CLI client for Trello.

ВНИМАНИЕ: Перед запуском скрипта создайте в корневой директории файл auth_params.py с переменными
KEY = 'Ваш Trello ключ'
TOKEN = 'Ваш Trello токен'

ATTENTION: Before running script, create in root directory file auth_params.py with variables
KEY = 'Your Trello Key'
TOKEN = 'Your Trello Token'

COMMANDS:
Read a data: python trelloAPI.py
Create a new card in given list: python trelloAPI.py create_card "Card name" "List name"
Create a new list: python trelloAPI.py create_list "List name"
Move a card from one list to another: python trelloAPI.py move_card "Card name" "List name"
Delete a card: python trelloAPI.py delete_card "Card name"
