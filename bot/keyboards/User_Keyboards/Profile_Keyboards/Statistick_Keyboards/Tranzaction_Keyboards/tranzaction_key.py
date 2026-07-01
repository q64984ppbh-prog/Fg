from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_tranzaction_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Пополнений", callback_data='tranzaction_replenishment'),
                InlineKeyboardButton(text="🧾 Выводов", callback_data='tranzaction_withdraw')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='statistic_user')
            ]
        ]
    )
    return main