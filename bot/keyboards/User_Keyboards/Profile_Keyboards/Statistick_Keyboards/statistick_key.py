from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_statistick_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Транзакции", callback_data='tranzaction_profile', icon_custom_emoji_id='5332455502917949981')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='start_profile')
            ]
        ]
    )
    return main

def back_statistick_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='statistic_user')
            ]
        ]
    )
    return main