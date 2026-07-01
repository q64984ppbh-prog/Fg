# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

# other
from data.config import db
from utils.help_function import clean
from utils.logs_message import logs_out_referal_bonus
from keyboards.User_Keyboards.Profile_Keyboards.Referal_Keyboard.referal_keyboard import (
    start_bonus_referal_keyboard
)

router = Router()

@router.callback_query(F.data == 'send_ref_bonus_in_money')
async def call_send_ref_bonus_in_money(call: CallbackQuery):

    user_id = call.from_user.id
    message_id = call.message.message_id
    username = call.from_user.username
    first_name = call.from_user.first_name

    flag = await db.admin.get_value('Flag_Bonus_Ref')
    if flag == 0:
        await call.answer(text="❌ Конкурс не активен!", show_alert=True)
        return

    total_refs = await db.referals.count_referals(user_id)
    paid_refs = await db.referals.get_referal_actual_bonus(user_id)
    bonus_per_10 = float(await db.admin.get_value('Amount_Bonus_Ref'))

    unpaid_refs = max(total_refs - paid_refs, 0)
    groups_of_10 = unpaid_refs // 10
    refs_to_pay_now = groups_of_10 * 10
    out_balance = round(groups_of_10 * bonus_per_10, 2)

    if out_balance < bonus_per_10:
        await call.answer(f"⭐️ Вывод доступен от {bonus_per_10:.2f}$", show_alert=True)
        return

    await db.referals.add_referal_actual_bonus(user_id, refs_to_pay_now)
    await call.answer("✅ Мы проверим ваших рефералов и отправим вам ваш бонус!", show_alert=True)

    paid_refs_new = paid_refs + refs_to_pay_now
    unpaid_refs_new = max(total_refs - paid_refs_new, 0)
    groups_of_10_new = unpaid_refs_new // 10
    out_balance_new = round(groups_of_10_new * bonus_per_10, 2)
    ref_balance = await db.referals.get_referal_balance(user_id)
    turnover = await db.referals.get_referal_turnover_bonus(user_id)

    await call.bot.edit_message_text(
        chat_id=user_id,
        message_id=message_id,
        text= clean(f"""
            <b>🎁 Реферальный бонус</b>

            <blockquote><b>📗 В чем суть ❓</b>
            <i>Пригласите <b>10 рефералов</b> и получите <b>{bonus_per_10}$</b> на свой баланс!
            После выполнения условия вы сможете вывести бонусные средства.  

            ⚠️ Перед выплатой мы проверим рефералов на накрутку.  
            Если будут выявлены подозрительные или фейковые аккаунты — <b>бонус не будет начислен.</b></i></blockquote>

            💰 Реф. Баланс — <b>{ref_balance}$</b>
            👤 Рефералов — <b>{total_refs} чел.</b>
            🤝 Выплачено за <b>{paid_refs_new} чел.</b>
            💸 Заработано — <b>{turnover}$</b>"""),
        reply_markup=start_bonus_referal_keyboard(out_balance_new)
    )

    await logs_out_referal_bonus(username, first_name, user_id, out_balance, refs_to_pay_now, call.bot)
