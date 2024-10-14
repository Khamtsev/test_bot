import os
import requests
from dotenv import load_dotenv
from http import HTTPStatus
from telegram import Update
from telegram.ext import (filters, ApplicationBuilder, ContextTypes,
                          CommandHandler, MessageHandler)


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHERAPI_TOKEN = os.getenv('WEATHERAPI_TOKEN')
ENDPOINT = 'https://api.weatherapi.com/v1/current.json'
START_MESSAGE = ('Привет! Отправь мне название города, '
                 'чтобы узнать погоду в нем!')
ANSWER_MESSAGE = """{city}, местное время {time}.
Температура воздуха: {temp} °C, {condition}. Ощущается как {feels_like} °C.
Влажность: {humidity} %.
Давление: {pressure} мм.рт.ст.
Ветер: {wind} км/ч.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE
    )


def get_api_answer(city):
    """Получение ответа от эндпоинта."""
    try:
        response = requests.get(
            ENDPOINT,
            params={
                'key': WEATHERAPI_TOKEN,
                'q': city,
                'lang': 'ru'
                }
            )
        if response.status_code != HTTPStatus.OK:
            raise ConnectionError(
                f'Эндпоинт недоступен: {response.status_code}'
            )
        return response.json()
    except requests.RequestException as error:
        raise ConnectionError(f'Не удалось получить ответ: {error}')


async def send_weather(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка сообщения с погодой."""
    try:
        data = get_api_answer(update.message.text)
        city = data["location"]["name"]
        time = data["location"]["localtime"].split()[1]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feels_like = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        pressure = round(
            int(data["current"]["pressure_mb"]) * 0.75006375541921, )
        wind = data["current"]["wind_kph"]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ANSWER_MESSAGE.format(
                city=city,
                time=time,
                temp=temp,
                condition=condition.lower(),
                feels_like=feels_like,
                humidity=humidity,
                pressure=pressure,
                wind=wind)
            )
    except ConnectionError as error:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Ошибка: {error}')
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Проверьте название города!')


def main() -> None:
    """Основная логика работы бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    send_weather_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),
                                          send_weather)
    application.add_handler(start_handler)
    application.add_handler(send_weather_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
