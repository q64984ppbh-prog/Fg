# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db

router = Router()

@router.callback_query(F.data.startswith('delete_referal_user_'))
async def call_delete_referal_user(call: CallbackQuery):

    user_id = call.from_user.id
    message_id = call.message.message_id

    data = call.data.split('_')
    player_id = int(data[3])

    referal_id = await db.referals.get_ref_id(player_id)

    if referal_id is None:
        await call.answer("❌ У него нет реферера для удаления.", show_alert=True)
        return

    await db.referals.delete_user_referal(player_id)
    await call.answer("✔ Реферал успешно удалён!", show_alert=True)