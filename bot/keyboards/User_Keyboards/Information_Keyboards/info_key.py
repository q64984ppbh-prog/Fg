from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import url_support, url_rules, url_channel_game, url_chat_game

def information_keybpard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨🏻‍💻 Поддержка", callback_data=url_support),
                InlineKeyboardButton(text="📚 Правила", callback_data=url_rules)
            ],
            [
                InlineKeyboardButton(text="💭 Чат", callback_data=url_chat_game),
                InlineKeyboardButton(text="🎲 Канал", callback_data=url_channel_game)
            ],
            [
                InlineKeyboardButton(text='⬅️ Вернуться', callback_data='back_start')
            ]
        ]
    )
    return main