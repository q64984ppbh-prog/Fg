# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Create_Game.mines_keyboard import start_mines_key

router = Router()

@router.callback_query(F.data == 'game_mines')
async def call_game_mines(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    count_mines = await db.game_mines.count_mines(user_id)

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        ℹ️ Выбрано: <b>💣 Мины</b>
                                        
                                        💰 Баланс: <b>{await db.users.get_balance(user_id):.2f}$</b>  
                                        💣 Мин: <b>{count_mines} шт.</b>
                                        
                                        <b>🎮 Начинаем игру?</b>"""),
                                        reply_markup=start_mines_key(count_mines))