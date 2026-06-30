# main
import random
from decimal import Decimal
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

# other
from data.config import db
from data.configure import minnes_kef
from utils.help_function import clean
from utils.function_bot import normal_chance
import handlers.Channel_Handler.channel_function as channel_functions
from keyboards.User_Keyboards.Create_Game.mines_keyboard import back_in_mines_game_key, generate_mines_field
from utils.logs_message import logs_create_mines_game

router = Router()
class StartMinesState(StatesGroup):

    amount = State()

@router.callback_query(F.data == 'start_game_mines')
async def call_start_game_mines(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🕹 Начало игры</b>
                                        
                                        💰 Баланс: <b>{await db.users.get_balance(user_id):.2f}$</b>  
                                        <b>✍🏻 Введите сумму ставки:</b>"""),
                                        reply_markup=back_in_mines_game_key())
    await state.set_state(StartMinesState.amount)

@router.message(StateFilter(StartMinesState.amount))
async def messgae_start_mines(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    try:
        amount = Decimal(message.text.strip().replace("$", "").replace(",", "."))
    except:
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    <b>🕹 Начало игры</b>
                                        
                                    💰 Баланс: <b>{await db.users.get_balance(user_id):.2f}$</b>  
                                    <b>❌ Введите верную сумму</b>"""),
                                    reply_markup=back_in_mines_game_key())
        return
    
    if amount < Decimal('0.2'):
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    <b>🕹 Начало игры</b>
                                     
                                    <blockquote>❌ Минимальная сумму депа: <b>{0.2}</b></blockquote>
                                        
                                    <b>ℹ️ Попробуйте еще раз</b>"""),
                                    reply_markup=back_in_mines_game_key())
        return
    
    await state.clear()
    if await db.users.try_reserve_balance(user_id, amount):
        count_mines = await db.game_mines.count_mines(user_id) # СКОКА МИН У ЧЕЛА

        value = await logs_create_mines_game(user_id, username, first_name, count_mines, amount, message.bot)
        game_id = await db.game_mines.create_mines_game(user_id, value, count_mines)

        await db.users.add_turnover(user_id, value)
        await channel_functions.check_user_level_up(user_id, message.bot)

        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                     <b>🕹 Игра #{game_id} запущена</b>
                                     
                                     💣 Мин: <b>{count_mines} шт.</b>
                                     💰 Ставка: <b>{value:.2f}$</b>
                                                   
                                     ℹ️ Выберите клетку для <b>открытия</b>"""),
                                     reply_markup=generate_mines_field(game_id))

    else:
        photo = FSInputFile('photo/start.jpg')
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    <b>🕹 Начало игры</b>
                                        
                                    💰 Баланс: <b>{await db.users.get_balance(user_id):.2f}$</b>  
                                    <b>❌ На балансе недостаточно средств</b>"""),
                                    reply_markup=back_in_mines_game_key())
        
import random

@router.callback_query(F.data.startswith("open_cell:"))
async def open_cell_handler(call: CallbackQuery):

    _, game_id, cell = call.data.split(":")
    game_id = int(game_id)
    cell = int(cell)
    user_id = call.from_user.id

    game = await db.game_mines.get_game(game_id)
    if not game:
        await call.answer("❌ Игра не найдена", show_alert=True)
        return

    if game.get("status") != "active":
        await call.answer("❌ Игра уже завершена!", show_alert=True)
        return

    opened = game["opened_cells"] or []
    mines = game["mines_position"] or []
    count_mines = game["mines_count"]
    bet_amount = float(game["amount"])

    if cell in opened:
        await call.answer("❌ Эта клетка уже открыта")
        return

    opened.append(cell)
    if cell not in mines:
        N = len(opened)
        M = count_mines
        chance_rtp = normal_chance(N, M)

        roll = random.uniform(0, 100)

        if roll <= chance_rtp:
            if mines:
                idx = random.randrange(len(mines))
                old_mine = mines[idx]
                mines[idx] = cell
            else:
                mines = [cell]

            await db.game_mines.update_mines(game_id, mines)

    exploded = cell in mines
    if exploded:
        await db.game_mines.open_cell(game_id, opened)
        await db.game_mines.finish_game(game_id)

        await call.message.edit_reply_markup(
            reply_markup=generate_mines_field(
                game_id,
                opened,
                mines,
                count_mines,
                bet_amount,
                finish=True,
                exploded=True
            )
        )
        await call.answer("💥 Вы попали на мину!", show_alert=True)
        return

    await db.game_mines.open_cell(game_id, opened)
    await call.message.edit_reply_markup(
        reply_markup=generate_mines_field(
            game_id,
            opened,
            mines,
            count_mines,
            bet_amount
        )
    )

    await call.answer()

@router.callback_query(F.data.startswith("take_prize:"))
async def take_prize_handler(call: CallbackQuery):

    _, game_id = call.data.split(":")
    game_id = int(game_id)
    user_id = call.from_user.id

    game = await db.game_mines.get_game(game_id)
    if not game:
        await call.answer("❌ Игра не найдена", show_alert=True)
        return

    if game.get("status") != "active":
        await call.answer("Игра уже завершена!", show_alert=True)
        return

    opened = game["opened_cells"] or []
    count_mines = game["mines_count"]
    bet_amount = float(game["amount"])
    mines = game["mines_position"] or []

    kef_list = minnes_kef.get(count_mines, [])
    if len(opened) < len(kef_list):
        kef = kef_list[len(opened)]
    else:
        kef = kef_list[-1] if kef_list else 0

    prize = bet_amount * kef

    await db.users.add_balance(user_id, prize)
    await db.game_mines.finish_game(game_id)

    await call.message.edit_reply_markup(
        reply_markup=generate_mines_field(
            game_id,
            opened,
            mines,
            count_mines,
            bet_amount,
            finish=True,
            exploded=False
        )
    )

    print(prize)
    await db.users.update_max_win(user_id, prize)
    await call.answer(f"🎁 Вы забрали {prize:.2f}$!", show_alert=True)