# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Create_Game.mines_keyboard import change_count_mines

router = Router()

@router.callback_query(F.data == 'change_count_mines')
async def call_change_count_mines(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    count = await db.game_mines.count_mines(user_id)

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>🎮 Выберите количество мин</b>
                                        
                                        <b>💣 Выбрано: {count} шт.</b>"""),
                                        reply_markup=change_count_mines(count))
    
@router.callback_query(F.data.startswith('mines_cho:'))
async def call_mines_cho(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if call.data.split(':')[1] == 'x':
        await call.answer('ℹ️ Выберите количество мин', show_alert=True)
        return

    mines_user = await db.game_mines.count_mines(user_id)
    data = call.data.split(':')
    mines_count = int(data[1])

    if mines_count == mines_user:
        await call.answer(f'💣 У вас уже выбрано {mines_count} мин.', show_alert=True)
        return
    
    await db.game_mines.update_count_mines(user_id, mines_count)
    mines_user = await db.game_mines.count_mines(user_id)

    await call.answer(f"💣 Вы установили {mines_count} мин.", show_alert=True)
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>🎮 Выберите количество мин</b>
                                        
                                        <b>💣 Выбрано: {mines_user} шт.</b>"""),
                                        reply_markup=change_count_mines(mines_user))