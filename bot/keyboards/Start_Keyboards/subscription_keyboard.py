from typing import List, Tuple
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

def markup_channels(channels, ref_code=None):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []

    for i, (url, _, username) in enumerate(channels, start=1):
        row.append(InlineKeyboardButton(text=f"{username}", url=url))
        if i % 2 == 0:
            keyboard.inline_keyboard.append(row)
            row = []
    if row:
        keyboard.inline_keyboard.append(row)

    ref = ref_code or "none"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="✅ Проверить", callback_data=f"check_subscription:{ref}")
    ])
    return keyboard
