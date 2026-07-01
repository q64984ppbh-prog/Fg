from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_bonus_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛡 Лига", callback_data='league_bonus'),
                InlineKeyboardButton(text="🎁 Приписка", callback_data='pripiska_bonus')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='start_profile')
            ]
        ]
    )
    return main

def back_in_bonus_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='bonus_start')
            ]
        ]
    )
    return main