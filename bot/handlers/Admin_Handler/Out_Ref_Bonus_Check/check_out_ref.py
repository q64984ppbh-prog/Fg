# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from config_reader import config
from utils.help_function import clean
from keyboards.Admin_Keyboards.Logs_Keyboard.logs_keyboard import (
    link_url_support_failed,
    value_out_bonus
)

router = Router()

@router.callback_query(F.data.startswith("accept_go_send_bonus_ref"))
async def call_accept_go_send_bonus_ref(call: CallbackQuery):

    message_id = call.message.message_id

    data = call.data.split(':')
    pool_id = int(data[1])
    amount = float(data[2])

    await db.referals.add_referal_bonus_turnover(pool_id, amount)
    await db.admin.plus_admin_statistick('RefBonusCount', amount)
    await db.users.add_balance(pool_id, amount)

    await call.answer(caption="✅ Мы успешно выплатили пользователю бонус!", show_alert=True)
    await call.bot.edit_message_reply_markup(chat_id=config.logs_id,
                                             message_id=message_id,
                                             reply_markup=value_out_bonus(True))
    try:
        await call.bot.send_message(chat_id=pool_id,
                                    caption=clean(f"""
                                    👤 Ваш <b>бонус вывод</b> на <code>{amount}$</code> одобрен

                                    <blockquote>🎁 Деньги прийдут к вам на баланс, после чего вы можете ими управлять!</blockquote>

                                    👛 Баланс: <b>{await db.users.get_balance(pool_id)}$</b>

                                    <b>🤝 Приглашай больше друзей и зарабатывай вместе с нами!</b>"""))
    except:
        pass

@router.callback_query(F.data.startswith("failed_go_send_bonus_ref"))
async def call_failed_go_send_bonus_ref(call: CallbackQuery):

    message_id = call.message.message_id

    data = call.data.split(':')
    pool_id = int(data[1])
    amount = float(data[2])

    await call.answer(caption="❌ Мы отклонили заявку пользователя!", show_alert=True)
    await call.bot.edit_message_reply_markup(chat_id=config.logs_id,
                                             message_id=message_id,
                                             reply_markup=value_out_bonus(False))
    try:
        await call.bot.send_message(chat_id=pool_id,
                                    caption=clean(f"""
                                    🎁 Администрация отклонила ваш <b>бонусный вывод</b>

                                    <blockquote>ℹ️ Нам показалось что вы могли накрутить своих рефералов! Если это не так, обратитесь в поддержку!</blockquote>
                                               
                                    <b>🤝 Приглашай больше друзей и зарабатывай вместе с нами!</b>"""),
                                    reply_markup=link_url_support_failed())
    except:
        pass