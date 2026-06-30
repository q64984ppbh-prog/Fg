# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.start_admin_keyboard import back_in_admin_keyboard

router = Router()

@router.callback_query(F.data == 'statistics_project')
async def call_statistics_project_admin(call: CallbackQuery):

    user_id = call.from_user.id
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        return

    await call.answer()

    stats = await db.admin.get_all_statistics()
    total_users = await db.admin.get_total_users()
    turnover = await db.admin.get_total_turnover()
    wins, loses = await db.admin.get_win_lose_stats()

    text = clean(f"""
    <b>📊 Статистика проекта

    <blockquote>👤 Всего пользователей: <code>{total_users} чел.</code>
    💸 Оборот проекта: <code>{turnover:.2f}$</code>

    📈 Победы игроков: <code>{wins} шт.</code>
    📉 Поражения игроков: <code>{loses} шт.</code>

    🏦 Финансы:
    ∙ Выведено всего: <code>{stats['Amount_Replenishment']}$</code>
    ∙ Выведено за день: <code>{stats['Amount_Replenishment_Day']}$</code>
    ∙ Всего пополнено: <code>{stats['Amount_Deposit']}$</code>

    🎁 Выплачено за реф: <code>{stats['RefBonusCount']}$</code>

    📈 Прибыль:
    ∙ За день: <code>{stats['ProfitDay']}$</code>
    ∙ За неделю: <code>{stats['ProfitWeek']}$</code>
    ∙ Всего: <code>{stats['Profit']}$</code></blockquote></b>""")

    await call.bot.edit_message_caption(
        chat_id=user_id,
        message_id=message_id,
        caption=text,
        reply_markup=back_in_admin_keyboard()
    )
