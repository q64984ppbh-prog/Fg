from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_nav_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💸 Баланс"),
                KeyboardButton(text="🎮 Играть"),
                KeyboardButton(text="🏠 Меню")
            ]
        ],
        resize_keyboard=True
    )
