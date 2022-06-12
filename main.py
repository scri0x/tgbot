import logging
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, Dispatcher, executor, types
import db_request as db
import all_buttons as bt
from navigate import register_handlers_subjects
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.types import BotCommand
import config as conf

logger = logging.getLogger(__name__)


all_button = {'bkz': bt.subject_values_kz, 'bru': bt.subject_values_ru, 'mkz': bt.magistracy_buttons_kz,
              'mru': bt.magistracy_buttons_ru, 'dkz': bt.doctoranture_buttons_kz, 'dru': bt.doctoranture_buttons_ru,
              'ckz': bt.college_buttons_kz, 'cru': bt.college_buttons_ru, 'pkz': bt.subject_price_kz,
              'pru': bt.subject_price_ru}
lang = db.get_lang




async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/kz", description="Тілді қазақ тіліне өзгерту"),
        BotCommand(command="/ru", description="Изменить язык на русский"),
        BotCommand(command="/menu", description="Меню")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    config = conf.load_config("bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_subjects(dp)

    # @dp.message_handler(lambda message: any(map(message.text.lower().__contains__, bt.subject_short_ru)) and not any(
    #     map(message.text.lower().__contains__, ['-', 'экзамен', 'емтихан'])))
    # async def cmd_all(message: types.message):
    #     buttons = bt.button_from_short_subject(message.text)
    #     keyboard = types.InlineKeyboardMarkup(row_width=1)
    #     keyboard.add(*buttons)
    #     match lang:
    #         case "kz":
    #             await message.answer("Бейіндік пәндерді таңдаңыз", reply_markup=keyboard)
    #         case "ru":
    #             await message.answer("Выберите один профильный предмет", reply_markup=keyboard)

    @dp.errors_handler(exception=BotBlocked)
    async def error_bot_blocked(update: types.Update, exception: BotBlocked):
        # Update: объект события от Telegram. Exception: объект исключения
        # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
        print(f"Error: {exception}")
        db.delete_user(update.callback_query.from_user.id)
        return True

    await set_commands(bot)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
