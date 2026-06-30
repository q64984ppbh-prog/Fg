from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_tranzaction_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Пополнений", callback_data='tranzaction_replenishment'),
                InlineKeyboardButton(text="🧾 Выводов", callback_data='tranzaction_withdraw')
            ],
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='statistic_user')
            ]
        ]
    )
    return main