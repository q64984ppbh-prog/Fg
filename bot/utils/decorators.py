from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)
from aiogram import Bot
from functools import wraps
from data.config import db
from config_reader import config
from keyboards.Start_Keyboards.subscription_keyboard import markup_channels

async def check_channels(user_id: int, bot: Bot):
    channels = await db.channels.get_channels()
    unsubscribed_channels = []
    failed_channels = []

    for channel in channels:
        try:
            url, channel_id, username = channel
            chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if chat_member.status == 'left':
                unsubscribed_channels.append((url, channel_id, username))
        except Exception:
            failed_channels.append((url, channel_id, username))

    if failed_channels:
        for _, _, username in failed_channels:
            await db.channels.remove_channel_from_bd(username)

        failed_usernames = ", ".join(username for _, _, username in failed_channels)
        await bot.send_message(
            config.admin_id,
            f"<b>👉🏻 Бот не смог проверить каналы (удалены):</b>\n\n<blockquote><b>{failed_usernames}</b></blockquote>",
            parse_mode="HTML"
        )

    if unsubscribed_channels:
        return False, unsubscribed_channels
    return True, []


def require_subscription():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(event, *args, **kwargs):
            if isinstance(event, Message):
                user_id = event.from_user.id
                bot: Bot = event.bot
            elif isinstance(event, CallbackQuery):
                user_id = event.from_user.id
                bot: Bot = event.message.bot
            else:
                raise TypeError("rr")

            is_subscribed, unsubscribed_channels = await check_channels(user_id, bot)

            if not is_subscribed:
                keyboard = markup_channels(unsubscribed_channels)
                photo = FSInputFile('photo/start.jpg')

                if isinstance(event, Message):
                    await bot.send_photo(chat_id=user_id, photo=photo, text="<b>🚫 Чтобы продолжить, подпишитесь на каналы ниже:</b>", reply_markup=keyboard)

                elif isinstance(event, CallbackQuery):
                    await bot.edit_message_caption(chat_id=user_id, message_id=event.message.message_id, text="<b>🚫 Чтобы продолжить, подпишитесь на каналы ниже:</b>", reply_markup=keyboard)

                return

            return await handler(event, *args, **kwargs)
        return wrapper
    return decorator