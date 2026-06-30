from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import username_bot_casino, url_support, url_bot

def select_logs_out_ref_bonus(user_id, amount):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f'accept_go_send_bonus_ref:{user_id}:{amount}'),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f'failed_go_send_bonus_ref:{user_id}:{amount}')
            ],
            [
                InlineKeyboardButton(text="👁 Просмотр рефералов", url=f"http://t.me/{username_bot_casino}?start=checkreferaladmin_{user_id}")
            ]
        ]
    )
    return main

def value_out_bonus(flag: bool):
    if flag:
        main = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Выплачено!", callback_data='nool')
                ]
            ]
        )
    else:
        main = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Отказано!", callback_data='nool')
                ]
            ]
        )
    return main

def link_url_support_failed():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=url_support)
            ]
        ]
    )
    return 


def ling_game_bot():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💣 Играть", url=url_bot)
            ]
        ]
    )
    return main

def referals_keyboard(referals, page, per_page, owner_id, safe=False):
    start = (page - 1) * per_page
    end = start + per_page

    page_items = referals[start:end]
    total_pages = (len(referals) - 1) // per_page + 1

    keyboard = []

    for ref in page_items:
        username = ref["username"] or ref["first_name"] or "Без имени"
        user_id = ref["user_id"]

        if ref["username"]:
            button = InlineKeyboardButton(
                text=f"👤 @{ref['username']}",
                url=f"https://t.me/{ref['username']}"
            )
        else:
            if safe:
                button = InlineKeyboardButton(
                    text=f"👤 {username}",
                    callback_data=f"ref_info:{user_id}"
                )
            else:
                button = InlineKeyboardButton(
                    text=f"👤 {username}",
                    url=f"tg://user?id={user_id}"
                )

        keyboard.append([button])

    prev_page = page - 1 if page > 1 else total_pages
    next_page = page + 1 if page < total_pages else 1

    keyboard.append([
        InlineKeyboardButton(text="⬅", callback_data=f"ref_page:{owner_id}:{prev_page}"),
        InlineKeyboardButton(text="➡", callback_data=f"ref_page:{owner_id}:{next_page}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


