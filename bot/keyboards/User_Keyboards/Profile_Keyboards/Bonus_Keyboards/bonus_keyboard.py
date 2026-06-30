from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_bonus_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛡 Лига", callback_data='league_bonus'),
                InlineKeyboardButton(text="🎁 Приписка", callback_data='pripiska_bonus')
            ],
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='start_profile')
            ]
        ]
    )
    return main

def back_in_bonus_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='bonus_start')
            ]
        ]
    )
    return main