from aiogram.types import Message
from core import dp
from bot.find_regatta import find_states


@dp.message_handler(commands=['help', 'start'])
async def send_menu(message: Message):
    await message.reply(text='''Доступные команды: \n
    /help - подсказки по командам; \n
    /find - найти регату''', reply=False)


@dp.message_handler()
async def menu(message: Message):
    await message.reply(text='''Доступные команды:
        /help - подсказки по командам; \n
        /find - найти регату''', reply=False)
