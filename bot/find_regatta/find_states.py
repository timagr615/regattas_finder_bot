import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile
from core import dp, bot
from bot.find_regatta.find_response import date_response, name_response, text_answer
from bot.find_regatta.pdf_response import pdf_table
from db.utils import *


class Find(StatesGroup):
    boat = State()
    filt = State()
    filter_type = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Прервать выбор настроек
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Прекращено.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands='find')
async def process_find(message: Message):
    await Find.boat.set()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add('470', 'Laser', 'Laser Radial', '49er', '49er FX')
    await message.reply("Веберите класс яхт", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ['470', 'Laser', 'Laser Radial', '49er', '49er FX'],
                    state=Find.boat)
async def boat_invalid(message: Message):
    return await message.reply("Выберите класс яхты с кнопки.")


@dp.message_handler(lambda message: message.text, state=Find.boat)
async def process_filter(message: Message, state: FSMContext):
    """
    Обработка фильтра пользователя
    """
    async with state.proxy() as data:
        data['boat'] = message.text

    await Find.next()
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Выбрать период времени", "Поиск по названию")
    await message.reply("Выберите способ поиска соревнования", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Выбрать период времени", "Поиск по названию"],
                    state=Find.filt)
async def filter_invalid(message: Message):
    return await message.reply("Выберите способ поиска с кнопки.")


@dp.message_handler(lambda message: message.text, state=Find.filt)
async def process_filter(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['filt'] = message.text
    ReplyKeyboardRemove()
    await Find.next()
    if message.text == 'Выбрать период времени':
        murkup = ReplyKeyboardMarkup()
        murkup.add('Январь-Март', 'Апрель-Июнь', 'Июль-Сентябрь', 'Октябрь-Декабрь', 'Весь год')
        await message.reply(message.text, reply=False, reply_markup=murkup)
    else:
        await message.reply("Введите и отправьте слово из названия соревнования", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text, state=Find.filter_type)
async def process_filter_type(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['filter_type'] = message.text
    if data['filter_type'] in ['Январь-Март', 'Апрель-Июнь', 'Июль-Сентябрь', 'Октябрь-Декабрь', 'Весь год']:
        responses = date_response(data)
        if responses:
            if len(responses) < 6:
                for r in responses:
                    await message.reply(text_answer(r), parse_mode='HTML', reply=False,
                                        reply_markup=ReplyKeyboardRemove())
            else:
                pdf_table(responses)
                # f = os.path.abspath(os.curdir) + '/event_table.pdf'
                await message.answer('В выбранный период слишком много соревнований. '
                                     'Вам будет отправлен pdf файл', reply_markup=ReplyKeyboardRemove())
                await bot.send_document(message.from_user.id, document=InputFile('event_table.pdf'))

        else:
            await message.reply('В выбранный период нет соревнований', reply_markup=ReplyKeyboardRemove())
    else:
        responses = name_response(data)
        if responses:
            if len(responses) < 6:
                for r in responses:
                    await message.reply(text_answer(r), parse_mode='HTML', reply=False,
                                        reply_markup=ReplyKeyboardRemove())
            else:
                pdf_table(responses)
                await message.answer('По выбранному имени слишком много соревнований. '
                                     'Вам будет отправлен pdf файл.', reply_markup=ReplyKeyboardRemove())
                await bot.send_document(message.from_user.id, document=InputFile('event_table.pdf'))

        else:
            await message.reply('По введённому названию ничего не найдено', reply_markup=ReplyKeyboardRemove())
    await state.finish()
