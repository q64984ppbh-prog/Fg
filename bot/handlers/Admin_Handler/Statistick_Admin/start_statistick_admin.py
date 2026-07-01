from aiogram import F, Router
from aiogram.types import CallbackQuery
from data.config import db
from utils.help_function import clean

router = Router()

@router.callback_query(F.data == 'statistics_project')
async def call_statistics_project_admin(call: CallbackQuery):
    user_id = call.from_user.id
    
    total_users = await db.users.get_total_users()
    profit = await db.admin.get_statistick('Profit')
    profit_day = await db.admin.get_statistick('ProfitDay')
    profit_week = await db.admin.get_statistick('ProfitWeek')
    amount_deposit = await db.admin.get_statistick('Amount_Deposit')
    amount_replenishment = await db.admin.get_statistick('Amount_Replenishment')
    amount_replenishment_day = await db.admin.get_statistick('Amount_Replenishment_Day')
    
    text = clean(f"""<b>📊 Статистика проекта</b>

👥 Всего игроков: <code>{total_users}</code>
💰 Профит: <code>{profit}</code>
📅 Профит за день: <code>{profit_day}</code>
📆 Профит за неделю: <code>{profit_week}</code>
💵 Сумма депозитов: <code>{amount_deposit}</code>
💸 Сумма пополнений: <code>{amount_replenishment}</code>
🔄 Пополнений за день: <code>{amount_replenishment_day}</code>""")
    
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(chat_id=user_id, text=text)
