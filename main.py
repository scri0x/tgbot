from cgitb import text
import logging
from operator import contains
from re import IGNORECASE
from tracemalloc import stop
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from os import getenv
from sys import exit
import db_request as db


import asyncio
import datetime

# Объект бота
bot_token = "5322427961:AAElTOBaFWlfxonWpzYRIO7TZK-JhtNuU0s"
#if not bot_token:
#    exit("Error: no token provided")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Physic
@dp.message_handler(lambda message: 'физ' in message.text.lower() and '-' not in message.text.lower())
async def cmd_phys(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Математика-Физика", callback_data='phys_math'),
        types.InlineKeyboardButton(text="Физика-Химия", callback_data='phys_chem'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# Math
@dp.message_handler(lambda message: 'мат' in message.text.lower() and '-' not in message.text.lower())
async def cmd_math(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Математика-Физика", callback_data='phys_math'),
        types.InlineKeyboardButton(text="Математика-География", callback_data='math_geo'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# Biology
@dp.message_handler(lambda message: 'био' in message.text.lower())
async def cmd_bio(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Биология-География", callback_data='bio_geo'),
        types.InlineKeyboardButton(text="Химия-Биология", callback_data='chem_bio'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# Chemistry
@dp.message_handler(lambda message: 'хим' in message.text.lower())
async def cmd_chem(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Физика-Химия", callback_data='phys_chem'),
        types.InlineKeyboardButton(text="Химия-Биология", callback_data='chem_bio'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# Geography
@dp.message_handler(lambda message: 'гео' in message.text.lower())
async def cmd_geo(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Биология-География", callback_data='bio_geo'),
        types.InlineKeyboardButton(text="География-Всемирная История", callback_data='geo_hist'),
        types.InlineKeyboardButton(text="География-Английский", callback_data='geo_eng'),
        types.InlineKeyboardButton(text="Математика-География", callback_data='math_geo'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# History
@dp.message_handler(lambda message: 'истор' in message.text.lower())
async def cmd_history(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="География-Всемирная История", callback_data='geo_hist'),
        types.InlineKeyboardButton(text="Всемирная История-Человек.Общество.Право",
                                   callback_data='hist_hsl'),

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# RusLang
@dp.message_handler(lambda message: 'русс' in message.text.lower())
async def cmd_rus_lang(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Русский Язык-Русская Литература", callback_data='rulang_rulit'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# KZLang
@dp.message_handler(lambda message: 'казах' in message.text.lower())
async def cmd_kz_lang(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Казахский Язык-Казахская Литература", callback_data='kzlang_kzlit'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# HSL
@dp.message_handler(lambda message: 'человек' in message.text.lower() or 'чоп' in message.text.lower())
async def cmd_hsl(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Всемирная История-Человек.Общество.Право",
                                   callback_data='hist_hsl'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


# Payment
@dp.message_handler(Text(contains="плата", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    await message.answer('<b>Биология-География</b>\n "Педагогика и Психология" - 443.400 тг в год\n "',
                         parse_mode='html')


# Magistracy
@dp.message_handler(Text(contains="магистр", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ["first", "second", "third", "chetvertyii",
               "pyatyi", "shestoi", "🔄Назад🔄"]
    keyboard.add(*buttons)
    await message.answer("👨🏻‍🎓Выберите специальность магистратуры👨🏻‍🎓", reply_markup=keyboard)


# Doctoral
@dp.message_handler(Text(contains="доктор", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ["first1", "second2", "third3", "chetvertyii4",
               "pyatyi5", "shestoi6", "🔄Назад🔄"]
    keyboard.add(*buttons)
    await message.answer("👨‍🔬Выберите специальность докторантуры👨‍🔬", reply_markup=keyboard)


# GrantsAndDiscount
@dp.message_handler(Text(contains="Внутренние гранты и скидки", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="100%", callback_data='100'),
        types.InlineKeyboardButton(text="50%", callback_data='50'),
        types.InlineKeyboardButton(text="25%", callback_data='25'),
        types.InlineKeyboardButton(text="20%", callback_data='20'),
        types.InlineKeyboardButton(text="10%", callback_data='10'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer("Выберите скидку", reply_markup=keyboard)


@dp.message_handler(commands="menu")
async def cmd_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ["📚Предметы📚", "💰Оплата💰", "❓Задать вопрос❓", "📋Внутренние гранты и скидки📋",
               "🏢Колледж ЕНТ Специальности🏢", "👨🏻‍🎓Специальности Магистратуры👨🏻‍🎓",
               "👨‍🔬Специальности Докторантуры👨‍🔬"]
    keyboard.add(*buttons)
    await message.answer("Здравствуйте, Коркыт Ата бот приветствует вас🙋‍♂️\nВыберите действие",
                         reply_markup=keyboard)


# Ask a Question
@dp.message_handler(Text(contains="вопрос", ignore_case=True))
async def cmd_ask_ques(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Напишите нам на WhatsApp", callback_data='100',
                                   url='http://wa.me/+77029224458'),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer("<a href='http://wa.me/+77029224458'><b>Напишите нам на WhatsApp</b></a>", parse_mode='html',
                         reply_markup=keyboard)


@dp.message_handler(Text(contains="предметы", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    buttons = ["Биология-География", "География-Всемирная История", "География-Английский",
               "Всемирная История-Человек.Общество.Право", "Казахский Язык-Казахская Литература", "Математика-Физика",
               "Математика-География", "Русский Язык-Русская Литература", "Химия-Биология",
               "Физика-Химия", "Английский Язык-Всемирная История", "Творческий экзамен", "🔄Назад🔄"]
    keyboard.add(*buttons)
    await message.answer("Выберите свои предметы", reply_markup=keyboard)


@dp.message_handler(Text(contains="назад", ignore_case=True))
async def cmd_back(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ["📚Предметы📚", "💰Оплата💰", "❓Задать вопрос❓", "📋Внутренние гранты и скидки📋",
               "🏢Колледж ЕНТ Специальности🏢", "👨🏻‍🎓Специальности Магистратуры👨🏻‍🎓",
               "👨‍🔬Специальности Докторантуры👨‍🔬"]
    keyboard.add(*buttons)
    await message.answer("Здравствуйте, Коркыт Ата бот приветствует вас🙋‍♂️\nВыберите действие",
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data in ["phys_math","phys_chem","math_geo","bio_geo","chem_bio","geo_hist","geo_eng",
"hist_hsl","rulang_rulit","kzlang_kzlit"]) #Нету eng_hist
@dp.message_handler(lambda message: message.text in ["Биология-География", "География-Всемирная История", "География-Английский",
               "Всемирная История-Человек.Общество.Право", "Казахский Язык-Казахская Литература", "Математика-Физика",
               "Математика-География", "Русский Язык-Русская Литература", "Химия-Биология",
               "Химия-Физика", "Английский Язык-Всемирная История", "Творческий экзамен"])
async def subject_balls(subject, year = None):

    inline_subject = {'phys_math': "Математика-Физика",'phys_chem':"Химия-Физика",'math_geo': "Математика-География",'bio_geo': "Биология-География",
    'chem_bio': "Химия-Биология",'geo_hist': "География-Всемирная История",'geo_eng': "География-Английский",'hist_hsl': "Всемирная История-Человек.Общество.Право",
    'rulang_rulit': "Русский Язык-Русская Литература",'kzlang_kzlit': "Казахский Язык-Казахская Литература"}

    subject_str = subject.text if str(type(subject)) == "<class 'aiogram.types.message.Message'>" else inline_subject[subject.data]
    if not year:
        now = datetime.datetime.now()
        year = now.year - 1
    data = db.subject_ball_from_bd(subject_str, year)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for list_year in data[1]:
        buttons.append(types.InlineKeyboardButton(text=f"{str(list_year[0])[5:]} год", callback_data=subject_str + ' ' + list_year[0]))
    keyboard.add(*buttons)
    await subject.answer(data[0],reply_markup=keyboard) if str(type(subject)) == "<class 'aiogram.types.message.Message'>" else await subject.message.answer(data[0],reply_markup=keyboard)

'''@dp.callback_query_handler(Text(contains='year_'))
async def year(call: types.CallbackQuery):
    data = call.data.split(' ')
    data[1] = int(str(data[1])[5:])
    asyncio.get_running_loop().create_task(server_cb_async(request))'''


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
