from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import username_bot_casino, db

async def forrmated_privatnost(user_id):
    if await db.users.get_anonimnost(user_id):
        return "🥷🏻 Приватность"
    else:
        return "👤 Приватность"


async def start_profile_keyboard(user_id):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📥 Пополнить', callback_data='add_balance'),
                InlineKeyboardButton(text='📤 Вывести', callback_data='withdraw_balance')
            ],
            [
                InlineKeyboardButton(text=f'{await forrmated_privatnost(user_id)}', callback_data='private_user'),
                InlineKeyboardButton(text='👥 Партнерка', callback_data='referal_program')
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data='statistic_user'),
                InlineKeyboardButton(text='🍭 Бонусы', callback_data='bonus_start')
            ],
            [
                InlineKeyboardButton(text='🔙 Вернуться', callback_data='back_start')
            ]
        ]
    )
    return main

def start_profile_message_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📥 Пополнить', url=f"http://t.me/{username_bot_casino}?start=dep"),
                InlineKeyboardButton(text='📤 Вывести', url=f"http://t.me/{username_bot_casino}?start=withdraw")
            ]
        ]
    )
    return main