from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Create_Game.mines_keyboard import start_mines_key

router = Router()

@router.callback_query(F.data == 'game_mines')
async def call_game_mines(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    count_mines = await db.game_mines.count_mines(user_id)
    balance = await db.users.get_balance(user_id)
    text = f"ℹ️ Выбрано: 💣 Мины\n\n💰 Баланс: {balance:.2f}$\n💣 Мин: {count_mines} шт.\n\n🎮 Начинаем игру?"
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(user_id, text, reply_markup=start_mines_key(count_mines))
