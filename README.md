### О проекте
Телеграм бот, присылающий погоду в городе по запросу.

Реализовано с помощью Python Telegram Bot 21.6.

### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Khamtsev/test_bot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv мenv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Зарегистрироваться на weatherapi.com и получить api токен.

Создать бота в телеграм через @BotFather и получить api токен.

Создать и заполнить .env файл по образцу .env.example

Запустить:

```
weatherbot.py
```


Автор: Денис Хамцев, [GitHub](https://github.com/Khamtsev).