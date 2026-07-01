from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_value_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📈 Мин. Деп", callback_data='settings_deposit_admin_minimal'),
                InlineKeyboardButton(text="📉 Макс. Деп", callback_data='settings_deposit_admin_maximal')
            ],
            [
                InlineKeyboardButton(text="💰 Минимальный вывод", callback_data='settings_minimal_withdraw_admin')
            ],
            [
                InlineKeyboardButton(text='🚀 Бонус за приписку ника', callback_data='settings_bonus_pripiska_admin')
            ],
            [
                InlineKeyboardButton(text="🔗 Реферальный процент", callback_data='settings_referal_precent')
            ],
            [
                InlineKeyboardButton(text="🫂 Реф. Вывод", callback_data='settings_minimal_referal_withdraw_admin'),
                InlineKeyboardButton(text="🎁 Реф. Бонус", callback_data='settings_bonus_referal_admin')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='admin_panel')
            ]
        ]
    )
    return main

def back_in_meni_value_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='edit_value_project')
            ]
        ]
    )
    return main

def start_referal_bonus_keyboard(flag):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💸 Реф.Бонус", callback_data='change_ref_bonus_amount'),
                InlineKeyboardButton(text=f"{'❌ Выключить' if flag == 1 else '✅ Запустить'}", callback_data='change_status_referal_bonus')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='edit_value_project')
            ]
        ]
    )
    return main

def back_in_meni_referal_bonus_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='settings_bonus_referal_admin')
            ]
        ]
    )
    return main

def start_nickname_bonus(flag):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{'❌ Выключить' if flag == 1 else '✅ Запустить'}", callback_data='change_status_nickname_bonus')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='edit_value_project')
            ]
        ]
    )
    return main