import logging
from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, Dispatcher, types
import db_request as db
from navigate import register_handlers_subjects
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.types import BotCommand
import config as conf

logger = logging.getLogger(__name__)


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
