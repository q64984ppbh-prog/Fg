from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from data.config import db
from keyboards.User_Keyboards.Profile_Keyboards.profile_keyboard import start_profile_keyboard, start_profile_message_keyboard

router = Router()

def get_progress_bar(current_turnover, required_turnover):
    try:
        ratio = min(float(current_turnover or 0) / float(required_turnover or 1), 1.0)
    except: ratio = 0
    filled = int(ratio * 5)
    if ratio >= 1.0: filled = 5
    percent = int(ratio * 100)
    bar = ""
    for i in range(5):
        if i == 0: bar += '<tg-emoji emoji-id="5220076146019814024">🟢</tg-emoji>' if filled > 0 else '<tg-emoji emoji-id="5217573356907283683">⚪</tg-emoji>'
        elif i == 4: bar += '<tg-emoji emoji-id="5220011356438153097">🟢</tg-emoji>'
        elif i < filled: bar += '<tg-emoji emoji-id="5219867260285373996">🟢</tg-emoji>'
        else: bar += '<tg-emoji emoji-id="5217544636460976774">⚪</tg-emoji>'
    if percent >= 100: bar = '<tg-emoji emoji-id="5217573356907283683">🟢</tg-emoji>' + bar[bar.find('>')+1:]
    return bar, percent

@router.callback_query(F.data == 'start_profile')
async def call_start_profile(call: CallbackQuery):
    bot = call.bot; user_id = call.from_user.id; username = call.from_user.username
    user = await db.users.get_user(user_id)
    await call.answer()
    level = await db.users.get_level_by_id(user['level_id'])
    next_level = await db.users.get_next_level(level['required_turnover'] if level else 0)
    level_name = level['name'] if level else "Новичок"
    next_name = next_level['name'] if next_level else "Мастер"
    required = next_level['required_turnover'] if next_level else user['turnover']
    progress_bar, progress_percent = get_progress_bar(user['turnover'], required)
    games_played = user['win_game'] + user['lose_game']
    text = (
        f'<blockquote><tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> @{username}</blockquote>\n\n'
        f'<tg-emoji emoji-id="5472363448404809929">👛</tg-emoji> <b>Баланс:</b> <code>{user["balance"]:.2f}</code><tg-emoji emoji-id="5197434882321567830">💵</tg-emoji>\n\n'
        f'<blockquote><b>Прогресс: {progress_percent}%</b>\n{progress_bar}\n'
        f'<tg-emoji emoji-id="5206712720350545928">🏆</tg-emoji> <b>{level_name}</b> → <tg-emoji emoji-id="5206421246689969742">🏆</tg-emoji> <b>{next_name}</b></blockquote>\n\n'
        f'<tg-emoji emoji-id="5258330865674494479">🍑</tg-emoji> <b>Оборот:</b> <code>{user["turnover"]:.2f}</code><tg-emoji emoji-id="5197434882321567830">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258508428212445001">🎮</tg-emoji> <b>Сыграно:</b> <code>{games_played} игр.</code>'
    )
    await call.message.delete()
    await bot.send_message(user_id, text, parse_mode='HTML', reply_markup=await start_profile_keyboard(user_id))

@router.message(F.text.casefold().in_(["профиль", "profile", "/profile", "/профиль"]))
async def message_profile_start(message: Message):
    user = await db.users.get_user(message.from_user.id)
    level = await db.users.get_level_by_id(user['level_id'])
    next_level = await db.users.get_next_level(level['required_turnover'] if level else 0)
    level_name = level['name'] if level else "Новичок"
    next_name = next_level['name'] if next_level else "Мастер"
    required = next_level['required_turnover'] if next_level else user['turnover']
    progress_bar, progress_percent = get_progress_bar(user['turnover'], required)
    games_played = user['win_game'] + user['lose_game']
    text = (
        f'<blockquote><tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> @{message.from_user.username}</blockquote>\n\n'
        f'<tg-emoji emoji-id="5472363448404809929">👛</tg-emoji> <b>Баланс:</b> <code>{user["balance"]:.2f}</code><tg-emoji emoji-id="5197434882321567830">💵</tg-emoji>\n\n'
        f'<blockquote><b>Прогресс: {progress_percent}%</b>\n{progress_bar}\n'
        f'<tg-emoji emoji-id="5206712720350545928">🏆</tg-emoji> <b>{level_name}</b> → <tg-emoji emoji-id="5206421246689969742">🏆</tg-emoji> <b>{next_name}</b></blockquote>\n\n'
        f'<tg-emoji emoji-id="5258330865674494479">🍑</tg-emoji> <b>Оборот:</b> <code>{user["turnover"]:.2f}</code><tg-emoji emoji-id="5197434882321567830">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258508428212445001">🎮</tg-emoji> <b>Сыграно:</b> <code>{games_played} игр.</code>'
    )
    await message.answer(text, parse_mode='HTML', reply_markup=start_profile_message_keyboard())
