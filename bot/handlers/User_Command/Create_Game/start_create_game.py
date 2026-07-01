from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random, asyncio
from data.config import db, channel_game_id
from data.configure import GAMES, BET_TRANSLATIONS, GAME_COEFFICIENTS
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message
from handlers.Channel_Handler.channel_function import get_game_coefficient

router = Router()

class BetStates(StatesGroup):
    waiting_amount = State()
    waiting_confirm = State()

async def get_last_bet(user_id):
    user = await db.users.get_user(user_id)
    return float(user.get('last_bet', 0) or 0)

def games_row_keyboard(selected=None):
    kb = []
    row = []
    for game_key, game in GAMES.items():
        emoji = game.get("emoji", "🎮")
        style = "primary" if game_key == selected else None
        row.append(InlineKeyboardButton(text=emoji, callback_data=f"game:{game_key}", style=style))
        if len(row) == 4:
            kb.append(row)
            row = []
    if row:
        kb.append(row)
    kb.append([InlineKeyboardButton(text="💣 Мины", callback_data="game_mines")])
    kb.append([InlineKeyboardButton(text="✏️ Изменить ставку", callback_data="change_bet_amount")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def big_game_keyboard(game_key):
    game = GAMES[game_key]
    title = game.get("title", game_key)
    kb = [[InlineKeyboardButton(text=title, callback_data="noop", style="primary")]]
    row = []
    for bet_key, bet_title in game["bets"].items():
        full_name = BET_TRANSLATIONS.get(bet_key, bet_key)
        coef = get_game_coefficient(full_name)
        row.append(InlineKeyboardButton(text=f"{bet_title} | x{coef}", callback_data=f"bet:{game_key}:{bet_key}"))
        if len(row) == 2:
            kb.append(row)
            row = []
    if row:
        kb.append(row)
    kb.append([InlineKeyboardButton(text="✏️ Изменить ставку", callback_data="change_bet_amount")])
    kb.append([InlineKeyboardButton(text="Назад", callback_data="back_to_games", icon_custom_emoji_id="5258236805890710909")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def make_game_text(balance, bet):
    return f"<b>Выбирайте игру или режим</b>\n\n<blockquote>Баланс: <code>{balance:.2f}</code><tg-emoji emoji-id=\"5197434882321567830\">💵</tg-emoji>\nСтавка: <code>{bet:.2f}</code><tg-emoji emoji-id=\"5197434882321567830\">💵</tg-emoji></blockquote>"

@router.callback_query(F.data == 'create_game')
async def call_create_game(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    user_id = call.from_user.id
    bet = await get_last_bet(user_id)
    balance = await db.users.get_balance(user_id)
    await call.bot.send_message(user_id, make_game_text(balance, bet), parse_mode='HTML', reply_markup=games_row_keyboard())

@router.callback_query(F.data == 'game_mines')
async def call_game_mines(call: CallbackQuery, state: FSMContext):
    await call.answer()
    from .Mines_Game.start_mines_game import call_game_mines as real_mines
    await real_mines(call, state)

@router.callback_query(F.data == 'change_bet_amount')
async def call_change_bet(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    balance = await db.users.get_balance(call.from_user.id)
    await call.bot.send_message(call.from_user.id, f"💰 Баланс: {balance:.2f}$\n\nВведите сумму ставки:")
    await state.set_state(BetStates.waiting_amount)

@router.callback_query(F.data == 'back_to_games')
async def call_back_to_games(call: CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    bet = await get_last_bet(user_id)
    balance = await db.users.get_balance(user_id)
    await call.message.edit_text(make_game_text(balance, bet), parse_mode='HTML', reply_markup=games_row_keyboard())

@router.message(BetStates.waiting_amount)
async def message_bet_amount(message: Message, state: FSMContext):
    import re
    raw = message.text.strip().lower()
    for word in ['баксы', 'баксов', 'бакс', 'доллары', 'долларов', 'доллар', 'usdt', '$', 'рублей', 'рубля', 'рубль']:
        raw = raw.replace(word, '')
    raw = raw.strip()
    try:
        amount = float(raw)
    except:
        await message.answer("❌ Введите корректную сумму")
        return
    if amount < 0.2:
        await message.answer("❌ Минимальная ставка: 0.20$")
        return
    if amount > await db.users.get_balance(message.from_user.id):
        await message.answer("❌ Недостаточно средств")
        return
    await db.users.set_last_bet(message.from_user.id, amount)
    await state.clear()
    bet = await get_last_bet(message.from_user.id)
    balance = await db.users.get_balance(message.from_user.id)
    await message.answer(make_game_text(balance, bet), parse_mode='HTML', reply_markup=games_row_keyboard())

@router.callback_query(F.data.startswith('game:'))
async def call_game_selected(call: CallbackQuery):
    game_key = call.data.split(':')[1]
    if game_key == 'mines':
        return
    await call.answer()
    user_id = call.from_user.id
    bet = await get_last_bet(user_id)
    balance = await db.users.get_balance(user_id)
    await call.message.edit_text(make_game_text(balance, bet), parse_mode='HTML', reply_markup=big_game_keyboard(game_key))

@router.callback_query(F.data.startswith('bet:'))
async def call_bet_confirm(call: CallbackQuery, state: FSMContext):
    parts = call.data.split(':')
    game_key, bet_key = parts[1], parts[2]
    game = GAMES[game_key]
    bet_title = game["bets"].get(bet_key, bet_key)
    full_bet_name = BET_TRANSLATIONS.get(bet_key, bet_key)
    user_id = call.from_user.id
    amount = await get_last_bet(user_id)
    if amount <= 0:
        await call.answer("Сначала установите ставку!", show_alert=True)
        return
    balance = await db.users.get_balance(user_id)
    if amount > balance:
        await call.answer("❌ Недостаточно средств!", show_alert=True)
        return
    await db.users.minus_balance(user_id, amount)
    await db.users.add_turnover(user_id, amount)
    await call.message.delete()
    msg = await call.message.answer("⏳ Ставка принята..")
    await state.clear()
    await play_game_in_chat(call.bot, user_id, game_key, full_bet_name, amount, call.from_user.first_name, game.get('title', game_key), bet_title, msg.message_id)

async def play_game_in_chat(bot, user_id, game_key, stavka, amount, name, game_title, bet_title, confirm_msg_id):
    try:
        info = await bot.get_chat(user_id)
        full_name = info.full_name or name
        has_pripiska = '@duckwins' in (info.first_name or '').lower() or '@duckwins' in (info.last_name or '').lower()
    except:
        full_name, has_pripiska = name, False
    bonus_text, actual_value = "", amount
    if has_pripiska:
        bonus = amount * 0.026
        actual_value = amount + bonus
        bonus_text = "\n🎁 Бонус 2.6% за приписку!"
    caption = f"❤️‍🔥 {full_name} поставил на {stavka}\n\n💳 Ставка: {actual_value:.2f}💵\n💎 Лига: 🚀 Rookie\n🧾 Оплата через 🤖 DuckWin{bonus_text}"
    try:
        channel_post = await bot.send_message(channel_game_id, caption, reply_markup=keyboard_in_game_message())
    except:
        channel_post = None
    emoji_map = {'cube': '🎲', 'cubes': '🎲', 'basket': '🏀', 'football': '⚽', 'darts': '🎯', 'bowling': '🎳'}
    try:
        dice_msg = await bot.send_dice(user_id, emoji=emoji_map.get(game_key, '🎲'))
        await asyncio.sleep(4)
        dice_value = dice_msg.dice.value
    except:
        await bot.send_message(user_id, "❌ Ошибка при броске.")
        return
    if channel_post:
        try:
            await bot.forward_message(channel_game_id, user_id, dice_msg.message_id)
        except:
            pass
    win = False
    if game_key in ['cube', 'cubes']:
        if stavka in ['чёт', 'чет']: win = dice_value % 2 == 0
        elif stavka in ['нечёт', 'нечет']: win = dice_value % 2 != 0
        elif stavka == 'больше': win = dice_value > 3
        elif stavka == 'меньше': win = dice_value < 4
        elif stavka in ['1', '2', '3', '4', '5', '6']: win = dice_value == int(stavka)
        else: win = random.choice([True, False])
    elif game_key == 'basket': win = dice_value >= 4 if 'гол' in stavka or 'попал' in stavka else dice_value < 4
    elif game_key == 'football': win = dice_value >= 4 if 'гол' in stavka or 'попал' in stavka else dice_value < 4
    elif game_key == 'bowling': win = dice_value >= 5
    else: win = random.choice([True, False])
    coef = 1.85
    for k, names in GAME_COEFFICIENTS.items():
        if isinstance(k, (int, float)) and stavka in names:
            coef = k
            break
    if win:
        win_amount = actual_value * coef
        await db.users.add_balance(user_id, win_amount)
        new_balance = await db.users.get_balance(user_id)
        win_text = (
            f"Победа в игре на {amount:.2f}<tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>\n"
            f"<tg-emoji emoji-id=\"5449503162849318231\">❌</tg-emoji>{coef} <tg-emoji emoji-id=\"5449683594425410231\">🔼</tg-emoji> Выигрыш {win_amount:.2f}<tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>\n\n"
            f"<tg-emoji emoji-id=\"5258204546391351475\">💰</tg-emoji> Баланс {new_balance:.2f}<tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>"
        )
        await bot.send_message(user_id, win_text, parse_mode='HTML')
        if channel_post:
            try:
                await bot.send_animation(channel_game_id('animation/win.mp4'), caption=f"☘️ Вы выиграли!\n\n💸 На ваш баланс было\nзачислено {win_amount:.2f}$ (x{coef})\n💰 Опробуй свою удачу вновь!", reply_markup=keyboard_in_game_message())
            except:
                await bot.send_message(channel_game_id, f"☘️ Победа! {full_name} выиграл {win_amount:.2f}$ (x{coef})")
    else:
        await bot.send_message(user_id, "🚫 Вы проиграли..\n\n😡 Не расстраивайтесь! Удача обязательно улыбнется вам!")
        if channel_post:
            try:
                await bot.send_animation(channel_game_id('animation/lose.MP4'), caption="🚫 Вы проиграли..\n\n😡 Не расстраивайтесь! Удача обязательно улыбнется вам!", reply_markup=keyboard_in_game_message())
            except:
                await bot.send_message(channel_game_id, f"🚫 {full_name} проиграл {actual_value:.2f}$")
    try:
        await bot.delete_message(user_id, confirm_msg_id)
    except:
        pass
