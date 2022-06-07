import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import message
from aiogram.utils.exceptions import BotBlocked
import all_buttons
import db_request as db
import datetime
import all_buttons as bt

# Объект бота
bot_token = "5322427961:AAElTOBaFWlfxonWpzYRIO7TZK-JhtNuU0s"
# if not bot_token:
#    exit("Error: no token provided")
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
all_button = {'bkz': bt.subject_values_kz, 'bru': bt.subject_values_ru, 'mkz': bt.magistracy_buttons_kz,
              'mru': bt.magistracy_buttons_ru, 'dkz': bt.doctoranture_buttons_kz, 'dru': bt.doctoranture_buttons_ru,
              'ckz': bt.college_buttons_kz, 'cru': bt.college_buttons_ru, 'pkz': bt.subject_price_kz,
              'pru': bt.subject_price_ru}
lang = db.get_lang


@dp.callback_query_handler(lambda call: call.data in ['/ru', '/kz'])
@dp.message_handler(commands=['ru', 'kz'])
async def language(user):
    match (str(type(user))):
        case "<class 'aiogram.types.message.Message'>":
            match user.text:
                case '/kz':
                    db.update_lang(user.from_user.id, 'kz')
                    await user.answer('казак')
                case '/ru':
                    db.update_lang(user.from_user.id, 'ru')
                    await user.answer('русский')
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":
            match user.data:
                case '/kz':
                    db.insert_users(user.from_user.id, 'kz')
                    await user.message.answer('сиз бизге подписаться еттиниз')
                case '/ru':
                    db.insert_users(user.from_user.id, 'ru')
                    await user.message.answer('вы на нас подписались')


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Русский Язык🇷🇺", callback_data='/ru'),
        types.InlineKeyboardButton(text="Қазақ тілі🇰🇿", callback_data='/kz'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Список доступных комманд: \n/ru \n/kz \n/menu\nЧто бы не писать команды вручную, мы добавили "
                         "кнопку слева от клавиатуры. Нажав на нее вы сможете выполнять эти команды.\nТак же наш бот "
                         "поможет вам узнать информацию о том или ином профильном предмете. Для этого достаточно "
                         "нажать на соответвующую кнопку, или написать название предмета"
                         "\n<b>Для начала выберите язык:</b>", reply_markup=keyboard, parse_mode='html')


@dp.message_handler(Text(contains="назад", ignore_case=True))
@dp.message_handler(commands="menu")
async def cmd_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons_ru = ["📚Предметы📚", "💰Оплата💰", "❓Задать вопрос❓", "📋Внутренние гранты и скидки📋",
                  "🏢Колледж ЕНТ Специальности🏢", "👨🏻‍🎓Специальности Магистратуры👨🏻‍🎓",
                  "👨‍🔬Специальности Докторантуры👨‍🔬"]
    buttons_kz = ["📚Менің таңдау пәндерім📚", "💰2021 жылғы оқу ақысы💰", "❓Сұрағыңыз бар ма?❓",
                  "📋Ішкі гранттар мен жеңілдіктер📋",
                  "🏢Колледж - ҰБТ - Мамандықтары🏢", "👨🏻‍🎓Магистратура мамандықтары👨🏻‍🎓",
                  "👨‍🔬Докторантура мамандықтары👨‍🔬"]
    match lang(message.from_user.id):
        case "kz":
            keyboard.add(*buttons_kz)
            await message.answer("Калай макалай", reply_markup=keyboard)
        case "ru":
            keyboard.add(*buttons_ru)
            await message.answer("Здравствуйте, Коркыт Ата бот приветствует вас🙋‍♂️\nВыберите действие",
                                 reply_markup=keyboard)


# Payment
@dp.message_handler(lambda message: any(map(message.text.lower().__contains__, ['плата', 'ақысы'])))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    buttons = all_button['p' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    ent: types.message_entity
    ent = ['dg', 'dfg']
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Пәнді таңдаңыз", reply_markup=keyboard, entities=ent)
        case "ru":
            await message.answer("Выберите свои предметы", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in all_button['p' + lang(message.from_user.id)])
async def price(message: types.Message):
    data = db.price(message.text[1:], lang(message.from_user.id))
    await message.answer(data)


# Magistracy
@dp.message_handler(Text(contains="магистр", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['m' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    match lang(message.from_user.id):
        case "kz":
            await message.answer("idk таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите idk", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in all_button['m' + lang(message.from_user.id)])
async def magistracy(message: types.Message):
    data = db.price(message.text, lang(message.from_user.id))
    await message.answer(data)


# Doctoral
@dp.message_handler(Text(contains="доктор", ignore_case=True))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['d' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    match lang(message.from_user.id):
        case 'kz':
            await message.answer('👨‍🔬Докторантура idk таңдаңыз👨‍🔬', reply_markup=keyboard)
        case 'ru':
            await message.answer("👨‍🔬Выберите специальность докторантуры👨‍🔬", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in all_button['d' + lang(message.from_user.id)])
async def magistracy(message: types.Message):
    data = db.magistracy(message.text, lang(message.from_user.id))
    await message.answer(data)


# College
@dp.message_handler(Text(contains="колледж", ignore_case=True))
async def college(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = all_button['c' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    match lang(message.from_user.id):
        case "kz":
            await message.answer("idk таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите idk", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in all_button['c' + lang(message.from_user.id)])
async def magistracy(message: types.Message):
    data = db.college(message.text, lang(message.from_user.id))
    await message.answer(data)


# GrantsAndDiscount
@dp.callback_query_handler((lambda call: call.data in ['100%', '50%', '25%', '20%', '10%']))
@dp.message_handler(lambda message: any(map(message.text.lower().__contains__, ['скидки', 'жеңілдік'])))
async def cmd_menu_items(call):
    buttons = bt.buttons_for_discount
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    match (str(type(call))):
        case "<class 'aiogram.types.message.Message'>":
            data = db.discount_drom_bd('100%', lang(call.from_user.id))
            await call.answer(text=data, reply_markup=keyboard)
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":  # Если предыдущий текст равен тексту на замену ОШИБКА
            data = db.discount_drom_bd(call.data, lang(call.from_user.id))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=data,
                                        reply_markup=keyboard)
            await bot.answer_callback_query(callback_query_id=call.id)


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


@dp.message_handler(lambda message: any(map(message.text.lower().__contains__, ['предметы', 'пәндер'])))
async def cmd_menu_items(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, )
    buttons = all_button['b' + lang(message.from_user.id)]
    keyboard.add(*buttons)
    keyboard.add('🔄Назад🔄')
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Пәнді таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите свои предметы", reply_markup=keyboard)


@dp.message_handler(lambda message: any(map(message.text.lower().__contains__, bt.subject_short_ru)) and not any(
    map(message.text.lower().__contains__, ['-', 'экзамен', 'емтихан'])))
async def cmd_all(message: types.message):
    buttons = bt.button_from_short_subject(message.text)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    match lang(message.from_user.id):
        case "kz":
            await message.answer("Бейіндік пәндерді таңдаңыз", reply_markup=keyboard)
        case "ru":
            await message.answer("Выберите один профильный предмет", reply_markup=keyboard)


@dp.callback_query_handler(
    lambda call: call.data.split('/')[0] in bt.subject_keys)  # хэндлер пример: geo_hist, geo_hist/2020
@dp.message_handler(lambda message: message.text in all_button[
    'b' + lang(message.from_user.id)])  # хэндлер пример: Математика-Физика, Қазақ тілі-Қазақ әдебиеті
async def subject_balls(user_press):
    keys = bt.subject_keys
    values = all_button['b' + lang(user_press.from_user.id)]

    match (str(type(user_press))):
        case "<class 'aiogram.types.message.Message'>":  # для типа message
            subject_and_year = user_press.text.split('/')
            otvet = user_press.answer
        case "<class 'aiogram.types.callback_query.CallbackQuery'>":  # для типа callback
            subject_and_year = user_press.data.split('/')
            subject_and_year[0] = values[keys.index(subject_and_year[0])]
            otvet = user_press.message.answer

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
    await otvet(data[0], reply_markup=keyboard)


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Error: {exception}")
    db.delete_user(update.callback_query.from_user.id)
    return True


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
