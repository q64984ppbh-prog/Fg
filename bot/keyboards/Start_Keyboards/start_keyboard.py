from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from data.config import (
    name_casino, 
    db, url_channel_game,
    url_chat_game, url_support, url_faw
)
async def start_keyboard_inline(user_id):
    if not await db.admin.admin_exists(user_id):
        main = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🎲 Сделать ставку 🎲", callback_data='create_game')
                ],
                [
                    InlineKeyboardButton(text='💬 Наш чат', url=url_chat_game),
                    InlineKeyboardButton(text='🛟 Помощь', url=url_support)
                ],
                [
                    InlineKeyboardButton(text='📕 Правила', url=url_faw),
                    InlineKeyboardButton(text='👤 Профиль', callback_data='start_profile')
                ]
            ]
        )
    else:
        main = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🎲 Сделать ставку 🎲", callback_data='create_game')
                ],
                [
                    InlineKeyboardButton(text='💬 Наш чат', url=url_chat_game),
                    InlineKeyboardButton(text='🛟 Помощь', url=url_support)
                ],
                [
                    InlineKeyboardButton(text='📕 Правила', url=url_faw),
                    InlineKeyboardButton(text='👤 Профиль', callback_data='start_profile')
                ],
                [
                    InlineKeyboardButton(text='👨🏻‍💻 Админ панель 👨🏻‍💻', callback_data='admin_panel')
                ]
            ]
        )
    return main