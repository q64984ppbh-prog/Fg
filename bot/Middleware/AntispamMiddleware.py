import asyncio
from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import SkipHandler

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit=2, interval=5, key_prefix='antiflood_'):
        self.limit = limit
        self.interval = interval
        self.prefix = key_prefix
        self.users = {}

    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id
        now = asyncio.get_event_loop().time()

        times = self.users.get(user_id, [])
        times = [t for t in times if now - t < self.interval]
        times.append(now)
        self.users[user_id] = times

        if len(times) > self.limit:
            raise SkipHandler()

        return await handler(event, data)