from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.configure import GAMES, BET_TRANSLATIONS
from data.config import url_channel_game
from handlers.Channel_Handler.channel_function import get_game_coefficient

def start_create_game() -> InlineKeyboardMarkup:
    keyboard = []

    keyboard.append([
        InlineKeyboardButton(
            text="💣 Мины",
            callback_data="game_mines"
        )
    ])

    row = []
    for game_key, game in GAMES.items():
        emoji = game.get("emoji", "🎮")

        row.append(
            InlineKeyboardButton(
                text=emoji,
                callback_data=f"game:{game_key}"
            )
        )

        if len(row) == 4:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Вернуться",
            callback_data="back_start"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_bets_keyboard(game_key: str) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    game = GAMES[game_key]

    for bet_key, bet_title in game["bets"].items():

        full_game_name = BET_TRANSLATIONS[bet_key]

        coef = get_game_coefficient(full_game_name)
        button_text = f"{bet_title} | ×{coef}"

        row.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"bet:{game_key}:{bet_key}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="⬅️ Вернуться", callback_data="create_game")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def succes_stavka_user(game_key: str, bet_key: str = None, amount: float = 0):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💸 Ваша ставка", url=url_channel_game)
            ],
            [
                InlineKeyboardButton(text="🔄 Повторить", callback_data=f"bet:{game_key}:{bet_key}" if bet_key else f"game:{game_key}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="create_game")
            ]
        ]
    )
    return main

def back_in_game_cho_key(game_key: str):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data=f"game:{game_key}")
            ]
        ]
    )
    return main