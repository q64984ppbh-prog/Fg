from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_profile_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Пополнить", callback_data='add_balance', icon_custom_emoji_id="5443127283898405358"),
            InlineKeyboardButton(text="Вывести", callback_data='withdraw_balance', icon_custom_emoji_id="5445355530111437729")
        ],
        [
            InlineKeyboardButton(text="Приватность", callback_data='anonimnost', icon_custom_emoji_id="5258011929993026890"),
            InlineKeyboardButton(text="Партнерка", callback_data='start_referal', icon_custom_emoji_id="5445221832074483553")
        ],
        [
            InlineKeyboardButton(text="Статистика", callback_data='statistic_user', icon_custom_emoji_id="5231200819986047254"),
            InlineKeyboardButton(text="Бонусы", callback_data='bonus_start', icon_custom_emoji_id="5193085063998224234")
        ],
        [
            InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data='back_start')
        ]
    ])

def start_profile_message_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Пополнить", callback_data='add_balance', icon_custom_emoji_id="5443127283898405358"),
            InlineKeyboardButton(text="Вывести", callback_data='withdraw_balance', icon_custom_emoji_id="5445355530111437729")
        ],
        [
            InlineKeyboardButton(text="Приватность", callback_data='anonimnost', icon_custom_emoji_id="5258011929993026890"),
            InlineKeyboardButton(text="Партнерка", callback_data='start_referal', icon_custom_emoji_id="5445221832074483553")
        ],
        [
            InlineKeyboardButton(text="Статистика", callback_data='statistic_user', icon_custom_emoji_id="5231200819986047254"),
            InlineKeyboardButton(text="Бонусы", callback_data='bonus_start', icon_custom_emoji_id="5193085063998224234")
        ],
        [
            InlineKeyboardButton(text="Транзакции", callback_data='tranzaction_profile', icon_custom_emoji_id="5332455502917949981")
        ]
    ])
