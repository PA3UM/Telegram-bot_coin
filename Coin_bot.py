import logging
from aiogram import Bot, Dispatcher, executor, types
from info import TOKEN, keys
import time
import datetime
from Extensions import ConvertionException, CryptoConverter


bot = Bot(token = TOKEN)
dp = Dispatcher(bot = bot)


@dp.message_handler(commands = ['help'])
async def help_handler(message: types.Message):
    text = 'Чтобы начать работать введите комманду боту в следующем формате: \n<имя валюты>\
<в какую валюту перевести>\
<колличество переводимой валюты>\n<Увидеть список всех доступных валют: /values >'
    await message.reply(text)

@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Привет, {user_full_name}!\n Для начала работы с ботом, напишите команду /help и прочтите анатацию!")

@dp.message_handler(commands = ['values'])
async def values_handler(message: types.Message):
    text = 'Список всех доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    await message.reply(text)

@dp.message_handler(content_types=['text'])
async def convert(message: types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException('Не верное количество значений.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        await message.reply(f'Ошибка пользователя\n{e}')
    except Exception as e:
        await message.reply(f'Не удалось обработать команду\n{e}')
    else:
        summa = float(total_base) * float(amount)
        texts = f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*** \nЦена {amount} {quote} в {base} - {summa}"
        await message.reply(texts)

if __name__ == '__main__':
    executor.start_polling(dp)

