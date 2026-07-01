from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest

class IgnoreMessageNotModifiedMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                return
            raise
