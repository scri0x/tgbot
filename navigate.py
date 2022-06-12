import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
import all_buttons as bt
import db_request as db
import sqlite3
import config as conf

config = conf.load_config("bot.ini")

# Объявление и инициализация объектов бота и диспетчера
bot = Bot(token=config.tg_bot.token)

lang = db.get_lang
all_button = {'bkz': bt.subject_values_kz, 'bru': bt.subject_values_ru, 'mkz': bt.magistracy_buttons_kz,
              'mru': bt.magistracy_buttons_ru, 'dkz': bt.doctoranture_buttons_kz, 'dru': bt.doctoranture_buttons_ru,
              'ckz': bt.college_buttons_kz, 'cru': bt.college_buttons_ru, 'pkz': bt.subject_price_kz,
              'pru': bt.subject_price_ru}

class start_wait(StatesGroup):
    waiting_for_lang = State()

class subject_wait(StatesGroup):
    waiting_for_subjects = State()


class price_wait(StatesGroup):
    waiting_for_subjects = State()


class magistracy_wait(StatesGroup):
    waiting_for_subjects = State()


class doctoranture_wait(StatesGroup):
    waiting_for_subjects = State()


class college_wait(StatesGroup):
    waiting_for_subjects = State()


async def cmd_discount(call):
    buttons = bt.buttons_for_discount
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    match (str(type(call))):
        case "<class 'aiogram.types.message.Message'>":
            data = db.discount_drom_bd('100%', lang(call.from_user.id))
            await call.answer(text=data, reply_markup=keyboard)
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":  # Если предыдущий текст равен тексту на замену ОШИБКА
            try:
                data = db.discount_drom_bd(call.data, lang(call.from_user.id))
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=data,
                                            reply_markup=keyboard)
                await bot.answer_callback_query(callback_query_id=call.id)
            except aiogram.utils.exceptions.MessageNotModified:
                await bot.answer_callback_query(callback_query_id=call.id)

async def cmd_menu_start(call: types.CallbackQuery,state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    match call.data:
        case '/kz':
            await db.insert_users(call.from_user.id, 'kz')
            await call.message.answer('Сіз қазақ тілін таңдадыңыз')
        case '/ru':
            await db.insert_users(call.from_user.id, 'ru')
            await call.message.answer('Вы выбрали русский язык')


    match lang(call.from_user.id):
        case "kz":
            keyboard.add(*bt.buttons_kz)
            await call.message.answer("Әрекетті таңдаңыз", reply_markup=keyboard)
        case "ru":
            keyboard.add(*bt.buttons_ru)
            await call.message.answer("Выберите действие", reply_markup=keyboard)
    await state.finish()
    await bot.answer_callback_query(callback_query_id=call.id)

async def cmd_menu(user_press: types.Message, state: FSMContext = None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    match lang(user_press.from_user.id):
        case "kz":
            keyboard.add(*bt.buttons_kz)
            await user_press.answer("Әрекетті таңдаңыз", reply_markup=keyboard)
        case "ru":
            keyboard.add(*bt.buttons_ru)
            await user_press.answer("Выберите действие", reply_markup=keyboard)

    if state != None:
        await state.finish()


async def cmd_subject_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    buttons = all_button['b' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Пәнді таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите свои предметы", reply_markup=keyboard)
    await subject_wait.waiting_for_subjects.set()


async def subject_balls(user_press):
    keys = bt.subject_keys
    values = all_button['b' + lang(user_press.from_user.id)]

    match (str(type(user_press))):
        case "<class 'aiogram.types.message.Message'>":  # для типа message
            if user_press.text not in all_button['b' + lang(user_press.from_user.id)]:
                return
            subject_and_year = user_press.text.split('/')
            otvet = user_press.answer
            answer_callback = None
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":  # для типа callback
            subject_and_year = user_press.data.split('/')
            subject_and_year[0] = values[keys.index(subject_and_year[0])]
            otvet = user_press.message.answer
            answer = bot.answer_callback_query(callback_query_id=user_press.id)

    try:
        subject_and_year[1]
    except IndexError:
        now = datetime.datetime.now()  # Ставить этот год
        subject_and_year.insert(1, now.year - 1)

    data = db.subject_ball_from_bd(subject_and_year[0], int(subject_and_year[1]),
                                   lang(user_press.from_user.id))  # Запрос на бд возвращает текст и года

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    year = {'kz': 'жыл', 'ru': 'год'}
    for list_year in data[1]:
        buttons.append(types.InlineKeyboardButton(text=f"{str(list_year[0])[5:]} {year[lang(user_press.from_user.id)]}",
                                                  callback_data=keys[values.index(subject_and_year[0])] + '/' + str(
                                                      list_year[0])[5:]))
    keyboard.add(*buttons)
    await otvet(data[0], reply_markup=keyboard, parse_mode="html")

    if answer:
        await answer


async def cmd_price_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    buttons = all_button['p' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Пәнді таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите свои предметы", reply_markup=keyboard)
    await price_wait.waiting_for_subjects.set()


async def price(message: types.Message, state: FSMContext):
    if message.text not in all_button['p' + lang(message.from_user.id)]:
        return
    data = db.price(message.text, lang(message.from_user.id))
    await message.answer(data, parse_mode="html")


async def cmd_magistracy_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['m' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case "kz":
            await message.answer("👨🏻‍🎓Магистратура мамандығын таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("👨🏻‍🎓Выберите специальность магистратуры", reply_markup=keyboard)
    await magistracy_wait.waiting_for_subjects.set()


async def magistracy(message: types.Message):
    if message.text not in all_button['m' + lang(message.from_user.id)]:
        return
    data = db.magistracy(message.text, lang(message.from_user.id))
    await message.answer(data, parse_mode="html")


async def cmd_doctoranture_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['d' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case 'kz':
            await message.answer('👨‍🔬Докторантура мамандығын таңдаңыз', reply_markup=keyboard)
        case 'ru':
            await message.answer("👨‍🔬Выберите специальность докторантуры", reply_markup=keyboard)
    await doctoranture_wait.waiting_for_subjects.set()


async def doctoranture(message: types.Message):
    if message.text not in all_button['d' + lang(message.from_user.id)]:
        return
    data = db.doctoranture(message.text, lang(message.from_user.id))
    await message.answer(data, parse_mode="html")


async def cmd_college_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['c' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case "kz":
            await message.answer("🏢Мамандықты таңдаңыз🏢", reply_markup=keyboard)
        case "ru":
            await message.answer("🏢Выберите специальность🏢", reply_markup=keyboard)
    await college_wait.waiting_for_subjects.set()


async def college(message: types.Message):
    if message.text not in all_button['c' + lang(message.from_user.id)]:
        return
    data = db.college(message.text, lang(message.from_user.id))
    await message.answer(data, parse_mode="html")


async def cmd_start(message: types.message):
    try:
        db.get_lang(message.from_user.id)
        await cmd_menu(message)
    except IndexError:
        buttons = [
            types.InlineKeyboardButton(text="🇷🇺Русский Язык🇷🇺", callback_data='/ru', ),
            types.InlineKeyboardButton(text="🇰🇿Қазақ тілі🇰🇿", callback_data='/kz'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer(
            "Список доступных комманд: \n/ru \n/kz \n/menu\nЧто бы не писать команды вручную, мы добавили "
            "кнопку слева от клавиатуры. Нажав на нее вы сможете выполнять эти команды.\nТак же наш бот "
            "поможет вам узнать информацию о том или ином профильном предмете. Для этого достаточно "
            "нажать на соответвующую кнопку, или написать название предмета"
            "\n<b>Для начала выберите язык:</b>", reply_markup=keyboard, parse_mode='html')
        await start_wait.waiting_for_lang.set()



async def language(user):
    match (str(type(user))):
        case "<class 'aiogram.types.message.Message'>":
            try:
                db.get_lang(user.from_user.id)
                match user.text:
                    case '/kz':
                        db.update_lang(user.from_user.id, 'kz')
                        await user.answer('Сіз қазақ тілін таңдадыңыз')
                    case '/ru':
                        db.update_lang(user.from_user.id, 'ru')
                        await user.answer('Вы выбрали русский язык')
                await cmd_menu(user)
            except IndexError:
                await user.answer("Вы не зарегистрированы. Введите команду '/start' и выберите язык")
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":
            try:
                match user.data:
                    case '/kz':
                        await db.insert_users(user.from_user.id, 'kz')
                        await user.message.answer('Сіз қазақ тілін таңдадыңыз')
                    case '/ru':
                        await db.insert_users(user.from_user.id, 'ru')
                        await user.message.answer('Вы выбрали русский язык')
                await cmd_menu(user)
            except sqlite3.IntegrityError:
                pass


async def cmd_ask_ques(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    match lang(message.from_user.id):
        case 'kz':
            buttons = [types.InlineKeyboardButton(text="Бізге WhatsApp-қа жазыңыз", callback_data='100',
                                                  url='http://wa.me/+77029224458')]
            keyboard.add(*buttons)
            await message.answer("<a href='http://wa.me/+77029224458'><b>Бізге WhatsApp-қа жазыңыз</b></a>",
                                 parse_mode='html', reply_markup=keyboard)
        case 'ru':
            buttons = [types.InlineKeyboardButton(text="Напишите нам на WhatsApp", callback_data='100',
                                                  url='http://wa.me/+77029224458')]
            keyboard.add(*buttons)
            await message.answer("<a href='http://wa.me/+77029224458'><b>Напишите нам на WhatsApp</b></a>",
                                 parse_mode='html', reply_markup=keyboard)


async def short_subject(message: types.message):
    buttons = bt.button_from_short_subject(message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Бейіндік пәндерді таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


def register_handlers_subjects(dp: Dispatcher):
    dp.register_message_handler(cmd_ask_ques, text=["❓Задать вопрос❓", "❓Сұрағыңыз бар ма?❓"])

    dp.register_message_handler(cmd_discount,
                                text=["📋Внутренние гранты и скидки📋", "📋Ішкі гранттар мен жеңілдіктер📋"],
                                state="*")
    dp.register_callback_query_handler(cmd_discount, lambda call: call.data in ['100%', '50%', '25%', '20%', '10%'])

    dp.register_message_handler(cmd_menu, text='🔄Назад🔄', state="*")
    dp.register_message_handler(cmd_menu, commands='menu', state="*")

    dp.register_message_handler(cmd_start, commands='start', state="*")
    dp.register_callback_query_handler(cmd_menu_start, state=start_wait.waiting_for_lang)

    dp.register_message_handler(language, commands=['ru', 'kz'], state="*")

    dp.register_message_handler(cmd_subject_items, text=['📚Предметы📚', '📚Менің таңдау пәндерім📚'], state="*")
    dp.register_message_handler(subject_balls, state=subject_wait.waiting_for_subjects)
    dp.register_callback_query_handler(subject_balls, lambda call: call.data.split('/')[0] in bt.subject_keys,
                                       state="*")

    dp.register_message_handler(cmd_price_items, text=['💰Оплата💰', '💰2021 жылғы оқу ақысы💰'], state="*")
    dp.register_message_handler(price, state=price_wait.waiting_for_subjects)

    dp.register_message_handler(cmd_magistracy_items, text=["👨🏻‍🎓Специальности Магистратуры👨🏻‍🎓",
                                                            "👨🏻‍🎓Магистратура мамандықтары👨🏻‍🎓"], state="*")
    dp.register_message_handler(magistracy, state=magistracy_wait.waiting_for_subjects)

    dp.register_message_handler(cmd_doctoranture_items, text=["👨‍🔬Специальности Докторантуры👨‍🔬",
                                                              "👨‍🔬Докторантура мамандықтары👨‍🔬"], state="*")
    dp.register_message_handler(doctoranture, state=doctoranture_wait.waiting_for_subjects)

    dp.register_message_handler(cmd_college_items, text=["🏢Колледж ЕНТ Специальности🏢",
                                                         "🏢Колледж - ҰБТ - Мамандықтары🏢"], state="*")
    dp.register_message_handler(college, state=college_wait.waiting_for_subjects)

    dp.register_message_handler(short_subject, lambda message: any(map(message.text.lower().__contains__, bt.subject_short)))