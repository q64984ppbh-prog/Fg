from aiogram import F, Router
from aiogram.types import CallbackQuery
from data.config import db
from keyboards.User_Keyboards.Profile_Keyboards.Statistick_Keyboards.Tranzaction_Keyboards.Deposit_Keyboard.deposit_key import generate_deposit_keyboard, back_deposit_keyboard

router = Router()

@router.callback_query(F.data == 'tranzaction_replenishment')
async def call_tranzaction_replenishment(call: CallbackQuery):
    user_id = call.from_user.id
    text = (
        f'<tg-emoji emoji-id="5258331647358540449">✍️</tg-emoji> <b>История пополнений</b>\n\n'
        f'<tg-emoji emoji-id="5258396243666681152">🔎</tg-emoji> Здесь отображается история всех ваших пополнений.\n'
        f'<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> <b>Что будем делать дальше?</b>'
    )
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(chat_id=user_id, text=text, parse_mode='HTML', reply_markup=await generate_deposit_keyboard(user_id))

@router.callback_query(F.data.startswith("historydeposit_"))
async def call_historydeposit_startswith(call: CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username
    data = call.data.split('_')
    deposit_id = data[1]
    date_deposit = await db.users.get_user_deposits_by_id(int(deposit_id))
    if not date_deposit:
        await call.answer("❌ Данная история депозита не найдена!", show_alert=True)
        return
    for dep in date_deposit:
        system_emoji = "🚀" if "xRocket" in dep['system'] else "👛"
        system_name = "xRocket" if "xRocket" in dep['system'] else "Crypto Bot"
        text = (
            f'<tg-emoji emoji-id="5361836987642815474">👛</tg-emoji> <b>Депозит #{deposit_id}</b>\n\n'
            f'<blockquote>┌ Игрок: @{username}\n'
            f'├ Айди: <code>{dep["user_id"]}</code>\n'
            f'├ Сумма: <code>{dep["amount"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>\n'
            f'├ Система: {system_name}\n'
            f'└ Дата: {dep["date"]}</blockquote>'
        )
        await call.answer()
        await call.message.delete()
        await call.bot.send_message(chat_id=user_id, text=text, parse_mode='HTML', reply_markup=back_deposit_keyboard())

@router.callback_query(lambda c: c.data.startswith("deposits_page_"))
async def paginate_deposits(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    keyboard = await generate_deposit_keyboard(callback.from_user.id, page=page)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=keyboard)
