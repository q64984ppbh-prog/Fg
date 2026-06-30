# main
from decimal import Decimal
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

# other
from data.config import db, url_channel_game
from data.configure import GAMES, BET_TRANSLATIONS
from utils.help_function import clean
import handlers.Channel_Handler.channel_function as channel_functions
from keyboards.User_Keyboards.Create_Game.start_create_game import create_bets_keyboard, back_in_game_cho_key, succes_stavka_user

router = Router()
class GameChannelState(StatesGroup):

    amount = State()
    
@router.callback_query(F.data.startswith("game:"))
async def open_game(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    game_key = call.data.split(":")[1]
    game = GAMES[game_key]

    await call.answer(game['emoji'])
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        ℹ️ Выбрано: <b>{game['title']}</b>

                                        <blockquote>💸 После оплаты, Ваша ставка сыграет в нашем игровом <b><a href='{url_channel_game}'>канале.</a></b></blockquote>"""),
                                        reply_markup=create_bets_keyboard(game_key))
    
@router.callback_query(F.data.startswith("bet:"))
async def call_bet(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    call_data = call.data.split(':')
    game_key = call_data[1]
    bet_key = call_data[2]

    game = GAMES[game_key]
    full_game_name = BET_TRANSLATIONS[bet_key]

    balance = await db.users.get_balance(user_id)
    if balance <= 0:
        await call.answer(f"❌ Ваш баланс равен 0.00$", show_alert=True)
        return

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        ℹ️ Выбрано: <b>{game['title']}</b>
                                        {game['emoji']} Игра: <b>{full_game_name}</b>

                                        <blockquote>💸 Введите сумму вашей ставки</blockquote>
                                        
                                        💰 Баланс: <b>{balance}$</b>"""),
                                        reply_markup=back_in_game_cho_key(game_key))
    await state.update_data(game_key=game_key, bet_key=bet_key)
    await state.set_state(GameChannelState.amount)

@router.message(StateFilter(GameChannelState.amount))
async def message_get_amount(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id
    first_name = message.from_user.first_name

    data = await state.get_data()
    game_key = data.get('game_key')
    bet_key = data.get('bet_key')

    game = GAMES[game_key]
    full_game_name = BET_TRANSLATIONS[bet_key]

    try:
        amount = Decimal(message.text)
    except:
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    ℹ️ Выбрано: <b>{game['title']}</b>
                                    {game['emoji']} Игра: <b>{full_game_name}</b>
                                     
                                    <blockquote>❌ Введите верную сумму</blockquote>
                                        
                                    <b>ℹ️ Попробуйте еще раз</b>"""),
                                    reply_markup=back_in_game_cho_key(game_key))
        return
    
    if await db.admin.get_value('Min_Dep') > amount:
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    ℹ️ Выбрано: <b>{game['title']}</b>
                                    {game['emoji']} Игра: <b>{full_game_name}</b>
                                     
                                    <blockquote>❌ Минимальная сумму депа: <b>{await db.admin.get_value('Min_Dep')}</b></blockquote>
                                        
                                    <b>ℹ️ Попробуйте еще раз</b>"""),
                                    reply_markup=back_in_game_cho_key(game_key))
        return

    if await db.users.try_reserve_balance(user_id=user_id, amount=amount):
        soo, valid, final_name, value = await channel_functions.check_reklama_user(first_name, full_game_name, amount, user_id, message.bot, True)
        if valid:
            if await channel_functions.handle_invalid_bet(full_game_name, value, soo, user_id, final_name, message.bot):
                await db.game_channel.add_bet_to_queue(final_name, user_id, value, full_game_name, soo)
                await db.users.add_turnover(user_id, value)
                await channel_functions.check_user_level_up(user_id, message.bot)

        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    ✅ Вы успешно поставили на: <b>{full_game_name}</b>
                                     
                                    <blockquote>🎲 Вы успешно поставили ставку, можете ее посмотреть в <a href='{url_channel_game}'>канале.</a></blockquote>
                                        
                                    💰 Баланс: <b>{await db.users.get_balance(user_id)}$</b>
                                    <b>ℹ️ Удача любит смелых — приходи и побеждай ещё раз!</b>"""),
                                    reply_markup=succes_stavka_user(game_key))
        await state.clear()
    else:
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    ℹ️ Выбрано: <b>{game['title']}</b>
                                    {game['emoji']} Игра: <b>{full_game_name}</b>
                                     
                                    <blockquote>❌ Произошла ошибка</blockquote>
                                        
                                    <b>ℹ️ На балансе недостаточно средств</b>"""),
                                    reply_markup=back_in_game_cho_key(game_key))
        await state.clear()