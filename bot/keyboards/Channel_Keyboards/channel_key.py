from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import url_check_channel, url_check_channel, username_bot_casino

def keyboard_error_user_id():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🎲 Сделать ставку', url=url_check_channel)
            ]
        ]
    )
    return main

def keyboard_in_game_message():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🎰 Сделать ставку', url=url_check_channel)
            ],
            [
                InlineKeyboardButton(text='💸 Забрать чек', url=f"http://t.me/{username_bot_casino}?start=withdraw")
            ]
        ]
    )
    return main