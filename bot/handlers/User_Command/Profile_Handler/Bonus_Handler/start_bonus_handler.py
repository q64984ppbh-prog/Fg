from aiogram import F, Router
from aiogram.types import CallbackQuery
from keyboards.User_Keyboards.Profile_Keyboards.Bonus_Keyboards.bonus_keyboard import start_bonus_keyboard

router = Router()

@router.callback_query(F.data == 'bonus_start')
async def call_bonus_start(call: CallbackQuery):
    text = (
        f'<tg-emoji emoji-id="5226731292334235524">🎁</tg-emoji> <b>Бонусы проекта</b>\n\n'
        f'<tg-emoji emoji-id="5172632227871196306">🌟</tg-emoji> Здесь вы можете узнать правила бонуса и проверить, активен ли он!\n'
        f'<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> <b>Выберите бонус:</b>'
    )
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=start_bonus_keyboard())
