# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Referal_Keyboard.referal_keyboard import (
    start_bonus_referal_keyboard
)

router = Router()

@router.callback_query(F.data == 'referal_go_bonus')
async def call_referal_go_bonus(call: CallbackQuery):

    user_id = call.from_user.id
    message_id = call.message.message_id

    flag = await db.admin.get_value("Flag_Bonus_Ref")
    if flag == 0:
        await call.answer(caption="❌ Конкурс не активен!", show_alert=True)
        return

    await call.answer()

    total_refs = await db.referals.count_referals(user_id)
    paid_refs = await db.referals.get_referal_actual_bonus(user_id)
    bonus_per_10 = float(await db.admin.get_value('Amount_Bonus_Ref'))

    unpaid_refs = max(total_refs - paid_refs, 0)
    groups_of_10 = unpaid_refs // 10
    out_balance = round(float(groups_of_10) * float(bonus_per_10), 2)

    await call.bot.edit_message_caption(
        chat_id=user_id,
        message_id=message_id,
        caption=clean(f"""
        <b>🎁 Реферальный бонус</b>

        <blockquote><b>📗 В чем суть ❓</b>
        <i>Пригласите <b>10 рефералов</b> и получите <b>{await db.admin.get_value('Amount_Bonus_Ref')}$</b> на свой баланс!
        После выполнения условия вы сможете вывести бонусные средства.  

        ⚠️ Однако <b>перед выплатой</b> мы проверим рефералов на накрутку.  
        Если будут выявлены подозрительные или фейковые аккаунты — <b>бонус не будет начислен.</b></i></blockquote>

        💰 Реф. Баланс — <b>{await db.referals.get_referal_balance(user_id)}$</b>
        👤 Рефералов — <b>{total_refs} чел.</b>
        🤝 Выплачено за <b>{paid_refs} чел.</b>
        💸 Заработанно — <b>{await db.referals.get_referal_turnover_bonus(user_id)}$</b>"""),
        reply_markup=start_bonus_referal_keyboard(out_balance)
    )
