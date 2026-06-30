from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import db
from math import ceil

async def generate_deposit_keyboard(user_id: int, page: int = 1) -> InlineKeyboardMarkup:
    deposits = await db.users.get_user_deposits(user_id)
    per_page = 5

    if not deposits:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📭 Нет пополнений", callback_data="none")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="tranzaction_profile")]
        ])
    
    deposits = list(reversed(deposits))

    total = len(deposits)
    total_pages = ceil(total / per_page)

    if page < 1:
        page = total_pages
    elif page > total_pages:
        page = 1

    start = (page - 1) * per_page
    end = start + per_page
    current_page_items = deposits[start:end]

    buttons = []
    for dep in current_page_items:
        text = f"#{dep['id']} {dep['system']} - {dep['amount']}$"
        buttons.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"historydeposit_{dep['id']}"
            )
        ])

    pagination_buttons = []
    if total_pages > 1:
        prev_page = page - 1 if page > 1 else total_pages
        next_page = page + 1 if page < total_pages else 1

        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"deposits_page_{prev_page}")
        )
        pagination_buttons.append(
            InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="none")
        )
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"deposits_page_{next_page}")
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    buttons.append([InlineKeyboardButton(text="⬅️ Вернуться", callback_data="tranzaction_profile")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_deposit_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='tranzaction_replenishment')
            ]
        ]
    )
    return main