from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.configure import minnes_kef

def start_mines_key(count_mines):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🕹 Начать игру", callback_data='start_game_mines')
            ],
            [
                InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data='create_game'),
                InlineKeyboardButton(text=f"💣 {count_mines}", callback_data='change_count_mines')
            ]
        ]
    )
    return main

def change_count_mines(count):

    keyboard = []
    row = []

    row.append(
        InlineKeyboardButton(text='X', callback_data='mines_cho:x')
    )

    for i in range(2,25):

        emoji = ''
        if i == count:
            emoji = '💣'

        row.append(
            InlineKeyboardButton(
                text=f"{i}{emoji}",
                callback_data=f'mines_cho:{i}'
            )
        )

        if len(row) == 6:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(
            text="Вернуться", icon_custom_emoji_id="5258236805890710909",
            callback_data="game_mines"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_in_mines_game_key():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='game_mines')
            ]
        ]
    )
    return main

def generate_mines_field(
    game_id: int,
    opened: list | None = None,
    mines: list | None = None,
    count_mines: int = 0,
    bet_amount: float = 0.0,
    finish: bool = False,
    exploded: bool = False
):
    field_size = 5
    opened = opened or []
    mines = mines or []

    if not finish:
        field = ['🌑' for _ in range(field_size * field_size)]
        for pos in opened:
            field[pos] = '🎁'
    else:
        field = ['📦' for _ in range(field_size * field_size)]

        for pos in mines:
            field[pos] = '💣'

        if exploded:
            for pos in opened:
                if pos in mines:
                    field[pos] = '💥'
                else:
                    field[pos] = '🎁'
        else:
            for pos in opened:
                field[pos] = '🎁'

    kef_list = minnes_kef.get(count_mines, [])
    if len(opened) < len(kef_list):
        kef = kef_list[len(opened)]
    else:
        kef = kef_list[-1] if kef_list else 0
        
    prize = bet_amount * kef
    keyboard, row = [], []

    for i in range(field_size * field_size):
        row.append(
            InlineKeyboardButton(
                text=field[i],
                callback_data=f"open_cell:{game_id}:{i}" if not finish else "disabled"
            )
        )
        if len(row) == field_size:
            keyboard.append(row)
            row = []

    if not finish:
        if len(opened) == 0:
            keyboard.append([
                InlineKeyboardButton(
                    text="ℹ️ Выберите клетку",
                    callback_data="disabled"
                )
            ])
        else:
            keyboard.append([
                InlineKeyboardButton(
                    text=f"🎁 Забрать {prize:.2f}$",
                    callback_data=f"take_prize:{game_id}"
                )
            ])
    else:
        keyboard.append([
            InlineKeyboardButton(
                text="🔄 Игра окончена",
                callback_data="disabled"
            ),
        ])
        keyboard.append([
            InlineKeyboardButton(
                text="Вернуться", icon_custom_emoji_id="5258236805890710909",
                callback_data='game_mines'
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)