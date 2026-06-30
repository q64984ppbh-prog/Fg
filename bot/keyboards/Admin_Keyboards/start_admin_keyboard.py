from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📕 Каналы", callback_data='channel_redact_project'),
         InlineKeyboardButton(text="📊 Статистика", callback_data='statistics_project')],
        [InlineKeyboardButton(text="👤 Найти игрока", callback_data='redact_user_statistics')],
        [InlineKeyboardButton(text="💭 Рассылка", callback_data='mailing_project'),
         InlineKeyboardButton(text="🛠 Значения", callback_data='edit_value_project')],
        [InlineKeyboardButton(text="🔑 Добавить аккаунт", callback_data='add_account_admin')],
        [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data='back_start')]
    ])

def back_in_admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data='admin_panel')]
    ])
