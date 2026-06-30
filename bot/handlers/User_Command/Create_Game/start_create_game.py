from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.config import db, url_channel_game
from utils.help_function import clean
from keyboards.User_Keyboards.Create_Game.start_create_game import start_create_game, create_bets_keyboard
from data.configure import GAMES, BET_TRANSLATIONS

router = Router()

class BetStates(StatesGroup):
    waiting_amount = State()
    waiting_confirm = State()

async def send_game_menu(bot, chat_id, message_id=None):
    kb = start_create_game()
    text = clean("<blockquote>☑️ Выберите игру, на которую хотите сделать ставку.</blockquote>")
    photo = FSInputFile('photo/start.jpg')
    if message_id:
        try:
            await bot.edit_message_media(chat_id=chat_id, message_id=message_id, media=InputMediaPhoto(media=photo, text=text), reply_markup=kb)
            return
        except:
            pass
    return await bot.send_message(chat_id=chat_id, text=text, reply_markup=kb)

@router.callback_query(F.data == 'create_game')
async def call_create_game(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await send_game_menu(call.bot, call.from_user.id)

@router.callback_query(F.data == 'game_mines')
async def call_game_mines(call: CallbackQuery, state: FSMContext):
    await call.answer("Мины загружаются...", show_alert=True)
    from .Mines_Game.start_mines_game import call_game_mines as real_mines
    await real_mines(call, state)

@router.callback_query(F.data.startswith('game:'))
async def call_game_selected(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    game_key = call.data.split(':')[1]
    if game_key == 'mines':
        return
    game = GAMES.get(game_key, {})
    game_title = game.get("title", game_key)
    await state.update_data(game_key=game_key, game_title=game_title)
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        chat_id=user_id,
        caption=clean(f"🎲 Ставка → <b>{game_title}</b>\n<blockquote>🎯 Выберите исход ставки:</blockquote>"),
        reply_markup=create_bets_keyboard(game_key)
    )

@router.callback_query(F.data.startswith('bet:'))
async def call_bet_selected(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    parts = call.data.split(':')
    game_key = parts[1]
    bet_key = parts[2]
    game = GAMES[game_key]
    game_title = game.get("title", game_key)
    bet_title = game["bets"].get(bet_key, bet_key)
    full_bet_name = BET_TRANSLATIONS.get(bet_key, bet_key)
    balance = await db.users.get_balance(user_id)
    
    await state.update_data(game_key=game_key, game_title=game_title, bet_key=bet_key, bet_title=bet_title, full_bet_name=full_bet_name)
    await state.set_state(BetStates.waiting_amount)
    
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        chat_id=user_id,
        caption=clean(f"🎲 Ставка → <b>{game_title}</b>\n🎯 Исход: <b>{bet_title}</b>\n👛 Баланс: <b>{balance:.2f}$</b>\n<blockquote>💸 Введите сумму вашей ставки.</blockquote>"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(caption="⬅️ Назад", callback_data=f"game:{game_key}")]])
    )

@router.message(BetStates.waiting_amount)
async def message_bet_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        amount = float(message.text.strip())
    except ValueError:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Введите корректное число</blockquote>")
        return
    if amount < 0.2:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Минимальная сумма ставки: 0.20$</blockquote>")
        return
    balance = await db.users.get_balance(user_id)
    if amount > balance:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Недостаточно средств\nВаш баланс: {balance:.2f}$</blockquote>")
        return
    
    data = await state.get_data()
    game_key = data['game_key']
    game_title = data['game_title']
    bet_title = data['bet_title']
    
    await state.update_data(amount=amount)
    await state.set_state(BetStates.waiting_confirm)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(caption="✅ Подтвердить", callback_data="confirm_bet")],
        [InlineKeyboardButton(caption="⬅️ Назад", callback_data=f"game:{game_key}")]
    ])
    
    await message.answer(
        clean(f"<b>Вы уверены?</b>\n<blockquote>🎲 Игра → {game_title}\n🎯 Исход → {bet_title}\n💰 Сумма: {amount:.2f}$</blockquote>"),
        reply_markup=kb
    )

@router.callback_query(F.data == 'confirm_bet', BetStates.waiting_confirm)
async def call_confirm_bet(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    game_key = data['game_key']
    bet_key = data['bet_key']
    amount = data['amount']
    full_bet_name = data['full_bet_name']
    
    balance = await db.users.get_balance(user_id)
    if amount > balance:
        await call.answer("❌ Недостаточно средств!", show_alert=True)
        return
    
    await db.users.minus_balance(user_id, amount)
    await db.users.add_turnover(user_id, amount)
    
    bet_id = await db.game_channel.add_bet_to_queue(
        name=call.from_user.first_name,
        user_id=user_id,
        value=amount,
        stavka=full_bet_name,
        message_id=call.message.message_id,
        source='bot'
    )
    
    channel_link = f"https://t.me/c/2514725444/{bet_id}"  # Обновится воркером
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(caption="💸 Ваша ставка", url=channel_link)],
        [InlineKeyboardButton(caption="🔄 Повторить", callback_data=f"bet:{game_key}:{bet_key}")],
        [InlineKeyboardButton(caption="⬅️ Назад", callback_data="create_game")]
    ])
    
    await call.message.delete()
    await call.message.answer(
        caption="💸",
        reply_markup=kb
    )
    await call.answer("✅ Ставка принята!", show_alert=False)
    await state.clear()
