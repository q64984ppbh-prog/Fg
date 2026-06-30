# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Bonus_Keyboards.bonus_keyboard  import (
    back_in_bonus_keyboard
)

router = Router()

@router.callback_query(F.data == 'league_bonus')
async def call_league_bonus(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    levels = await db.users.get_levels()
    caption = "🏆 <b>Лиги и бонусы</b>\n\n"
    for level in levels:

        turnover = int(level["required_turnover"])
        reward = int(level["reward"])

        caption += (
            f"<blockquote>{level['name']}</blockquote>\n"
            f"Оборот – <b>{turnover:,.2f}$</b>\n"
            f"Награда – <b>{reward}$</b>\n\n"
        )

    caption = caption.replace(",", " ")

    await call.answer()
    await call.bot.edit_message_caption(
        chat_id=user_id,
        message_id=message_id,
        caption=caption,
        reply_markup=back_in_bonus_keyboard()
    )