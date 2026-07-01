from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import db, url_chat_game, url_support, url_faw

async def start_keyboard_inline(user_id):
    kb = [
        [
            InlineKeyboardButton(text="Играть", callback_data='create_game', icon_custom_emoji_id="5258508428212445001"),
            InlineKeyboardButton(text="Чат", url=url_chat_game, icon_custom_emoji_id="5260535596941582167")
        ],
        [
            InlineKeyboardButton(text="Профиль", callback_data='start_profile', icon_custom_emoji_id="5886412370347036129"),
            InlineKeyboardButton(text="Партнерка", callback_data='start_referal', icon_custom_emoji_id="5967390100357648692")
        ],
        [
            InlineKeyboardButton(text="Правила", url=url_faw, icon_custom_emoji_id="5258503720928288433"),
            InlineKeyboardButton(text="Помощь", url=url_support, icon_custom_emoji_id="5931415565955503486")
        ]
    ]
    if await db.admin.admin_exists(user_id):
        kb.append([InlineKeyboardButton(text="Админ панель", callback_data='admin_panel')])
    return InlineKeyboardMarkup(inline_keyboard=kb)
