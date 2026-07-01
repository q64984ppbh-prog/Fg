from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from data.config import db
import math

router = Router()

@router.callback_query(F.data == 'tranzaction_profile')
async def call_tranzaction_profile(call: CallbackQuery):
    await show_transactions(call, 1)

async def show_transactions(call, page: int):
    user_id = call.from_user.id
    per_page = 10
    
    # Получаем историю депозитов и выводов
    deposits = await db.users.get_user_deposits(user_id)
    withdraws = await db.users.get_user_withdraw(user_id)
    
    # Объединяем и сортируем по дате
    transactions = []
    for d in (deposits or []):
        transactions.append({'type': 'deposit', 'amount': float(d['amount']), 'date': d['date']})
    for w in (withdraws or []):
        transactions.append({'type': 'withdraw', 'amount': float(w['amount']), 'date': w['date']})
    
    transactions.sort(key=lambda x: str(x['date']), reverse=True)
    
    total = len(transactions)
    total_pages = max(1, math.ceil(total / per_page))
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * per_page
    end = start + per_page
    page_items = transactions[start:end]
    
    text = f"<b><tg-emoji emoji-id=\"5330499265573695976\">↕️</tg-emoji> История транзакций · #{user_id}\n\n"
    
    for t in page_items:
        if t['type'] == 'deposit':
            text += f"<tg-emoji emoji-id=\"5327847754628609325\">↙️</tg-emoji> Депозит — {t['amount']:.2f} <tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>\n"
        else:
            text += f"<tg-emoji emoji-id=\"5330502087367212278\">↗️</tg-emoji> Вывод — {t['amount']:.2f} <tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>\n"
    
    text += "</b>"
    
    # Кнопки пагинации
    buttons = []
    if total_pages > 1:
        row = []
        if page > 1:
            row.append(InlineKeyboardButton(text="⬅️", callback_data=f"trx_page_{page-1}"))
        row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            row.append(InlineKeyboardButton(text="➡️", callback_data=f"trx_page_{page+1}"))
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(text="Назад", icon_custom_emoji_id="5258236805890710909", callback_data="statistic_user")])
    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    try:
        await call.message.edit_text(text, parse_mode='HTML', reply_markup=kb)
    except:
        await call.answer()
        await call.message.delete()
        await call.bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('trx_page_'))
async def paginate_transactions(call: CallbackQuery):
    page = int(call.data.split('_')[-1])
    await show_transactions(call, page)
