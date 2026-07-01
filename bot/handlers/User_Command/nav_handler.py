from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import re
from data.config import db
from keyboards.User_Keyboards.Profile_Keyboards.profile_keyboard import start_profile_keyboard
from keyboards.User_Keyboards.Create_Game.start_create_game import start_create_game as start_create_game_kb
from keyboards.Start_Keyboards.start_keyboard import start_keyboard_inline
from handlers.User_Command.Profile_Handler.start_profile_handler import get_progress_bar

router = Router()
BUTTONS = {'💸 Баланс', '🎮 Играть', '🏠 Меню'}

@router.message(F.text.regexp(r'^[\d.,]+\s*(?:$|баксы|баксов|бакс|доллары|долларов|доллар|usdt|\$)$', flags=re.IGNORECASE))
async def change_bet_global(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        return
    raw = message.text.strip().lower()
    for word in ['баксы', 'баксов', 'бакс', 'доллары', 'долларов', 'доллар', 'usdt', '$', ' ']:
        raw = raw.replace(word, '')
    try:
        amount = float(raw)
    except:
        return
    if amount < 0.2:
        return
    if amount > await db.users.get_balance(message.from_user.id):
        return
    await db.users.set_last_bet(message.from_user.id, amount)
    await state.clear()
    from handlers.User_Command.Create_Game.start_create_game import get_last_bet, games_row_keyboard
    bet = await get_last_bet(message.from_user.id)
    balance = await db.users.get_balance(message.from_user.id)
    txt = f"Выбирайте игру или режим\n\nБаланс: {balance:.2f}💵\nСтавка: {bet:.2f}💵"
    await message.answer(txt, reply_markup=games_row_keyboard())

@router.message(F.text.in_(BUTTONS))
async def navigation(message: Message, state: FSMContext):
    try:
        await state.clear()
    except:
        pass
    text = message.text

    if text == '💸 Баланс':
        user = await db.users.get_user(message.from_user.id)
        if not user:
            await message.answer("Сначала зарегистрируйтесь через /start")
            return
        level = await db.users.get_level_by_id(user['level_id'])
        next_level = await db.users.get_next_level(level['required_turnover'] if level else 0)
        level_name = level['name'] if level else "Новичок"
        next_name = next_level['name'] if next_level else "Мастер"
        required = next_level['required_turnover'] if next_level else user['turnover']
        progress_bar, progress_percent = get_progress_bar(user['turnover'], required)
        games_played = user['win_game'] + user['lose_game']
        txt = (
            f'👤 @{message.from_user.username}\n\n'
            f'👛 Баланс: {user["balance"]:.2f}\n\n'
            f'Прогресс: {progress_percent}%\n{progress_bar}\n'
            f'🏆 {level_name} → 🏆 {next_name}\n\n'
            f'🍑 Оборот: {user["turnover"]:.2f}\n'
            f'🎮 Сыграно: {games_played}'
        )
        await message.answer(txt, reply_markup=await start_profile_keyboard(message.from_user.id))
        return

    if text == '🎮 Играть':
        balance = await db.users.get_balance(message.from_user.id)
        from handlers.User_Command.Create_Game.start_create_game import get_last_bet, games_row_keyboard
        bet = await get_last_bet(message.from_user.id)
        txt = f"Выбирайте игру или режим\n\nБаланс: {balance:.2f}💵\nСтавка: {bet:.2f}💵"
        await message.answer(txt, reply_markup=games_row_keyboard())
        return

    if text == '🏠 Меню':
        user_id = message.from_user.id
        is_admin = await db.admin.admin_exists(user_id)
        admin_text = "<i>👨‍💻 Админ панель активна</i>" if is_admin else ""
        await message.answer(
            f"<tg-emoji emoji-id=\"4918354603281482671\">👋</tg-emoji> Добро пожаловать в @duckwin\n\n{admin_text}",
            parse_mode='HTML',
            reply_markup=await start_keyboard_inline(user_id)
        )
        return
