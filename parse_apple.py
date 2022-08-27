import logging
import requests
import psycopg2
from apple import parse
from humor import anecdot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
#ВНИМАНИЕ ЗДЕСЬ ПРОИСХОДИТ ИМПРОТ МОЕГО ТОКЕНА ИЗ ФАЙЛА CONFIG.PY У ВАС ЭТОГО ФАЙЛА НЕТ, ПОЭТОМУ ЛИБО СОЗДАЙТЕ И ЗАНЕСИТЕ ТОКЕН ТУДА 
#ЛИБО ПРОСТО УДАЛИ ЭТОТ ИМПОРТ  И ВСТАВЬ СВОЙ ТОКЕН НАПРЯМУЮ В ПЕРЕМЕННУЮ bot которая  ниже(12 строка)
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


def read_to_db(user_name,user_id,title,price):
    #ТУТ НУЖНО ВНЕСТИ ДАННЫЕ ОТ СВОЕЙ БАЗЫ 
    conn = psycopg2.connect(dbname='test',user='geo',password='12345',host='localhost')
    cursor =conn.cursor()
    cursor.execute('truncate tgtest cascade ;')
    cursor.execute("INSERT INTO tgtest(user_name ,user_id,title_mac,price) VALUES(%s,%s,%s,%s)",(user_name,user_id,title,price))
    conn.commit()
    cursor.close()
    conn.close()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Модели и цены🔫", "Курс валют💵", 'Рандомный анекдот😂']
    keyboard.add(*buttons)
    await message.answer("Что посмотрим?", reply_markup=keyboard)


@dp.message_handler(Text(equals='Модели и цены🔫'))
async def model_and_price(message: types.Message):
    result = parse()
    for name, price, image in result:
        read_to_db(str(message.from_user.first_name),str(message.from_user.id),name,price)
        await message.answer(f'{name}\n\n Цена: {price}\n{image}')

@dp.message_handler(Text(equals='Курс валют💵'))
async def dollar(message: types.Message):
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    dollar_rate = data['Valute']['USD']['Value']
    await message.answer(f'***КУРС ДОЛЛАРА***  {dollar_rate}')

@dp.message_handler(Text(equals='Рандомный анекдот😂'))
async def sugar(message: types.message.Message):
    await message.answer(anecdot())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)