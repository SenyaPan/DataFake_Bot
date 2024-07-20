### Установка

Создать venv
```bash
$ python3 -m venv <name of your virtual environment>
$ source <name of your virtual environment>/bin/activate

```

Установить библиотеки:

```bash
$ pip install -r requirements.txt
```
Потом создать .env файл и записать в него токен бота [TOKEN](https://core.telegram.org/bots/api), который можно достать из [bot](https://telegram.me/BotFather).

```bash
$ touch .env
$ echo "BOT_TOKEN=<your bot token>" >> .env
$ echo "IP_ADDRESS=<address of endpoint for analisis>" >> .env # здесь записывается адрес через локалхост
```

Также надо создать там же, где находится файл app.py, файл bot_feedback.txt в него будет записываться обратная связь пользователей 

Запустить бота из [app.py](app.py):

```bash
$ python app.py
```
