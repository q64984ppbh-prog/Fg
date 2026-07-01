from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_deposit_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏 Crypto Bot (3%)", callback_data='start_dep_cryptobot'),
                InlineKeyboardButton(text="🦋 xRocket (1%)", callback_data='start_dep_xrocket')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='start_profile')
            ]
        ]
    )
    return main

def back_in_deposit_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='add_balance')
            ]
        ]
    )
    return main

def deposit_message_keyboard(url):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏 Crypto Bot (3%)", url=url)
            ]
        ]
    )
    return main

def deposit_xrocket_message_keyboard(url):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🦋 xRocket (1%)", url=url)
            ]
        ]
    )
    return main