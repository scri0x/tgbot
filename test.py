from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class isBotBlocked(BoundFilter):
    key = 'is_bot_blocked'

    def __init__(self, is_bot_blocked: bool):
        self.is_bot_blocked = is_bot_blocked

    async def check(self, update: types.ChatMemberUpdated):
        return