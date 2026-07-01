from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_redact_channel_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖ Удалить", callback_data='channel_admin_dell'),
                InlineKeyboardButton(text="➕ Добавить", callback_data='channel_amin_add')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='admin_panel')
            ]
        ]
    )
    return main

def back_in_redact_channel_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Вернуться', callback_data='channel_redact_project')
            ]
        ]
    )
    return main