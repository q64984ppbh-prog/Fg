from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from data.config import db
from keyboards.User_Keyboards.Profile_Keyboards.Statistick_Keyboards.statistick_key import start_statistick_keyboard

router = Router()

@router.callback_query(F.data == 'statistic_user')
async def call_statistic_user(call: CallbackQuery):
    user = await db.users.get_user(call.from_user.id)
    text = (
        f'<blockquote><tg-emoji emoji-id="5258330865674494479">🍑</tg-emoji> <b>Статистика</b> @{call.from_user.username}</blockquote>\n\n'
        f'<tg-emoji emoji-id="5258204546391351475">💰</tg-emoji> <b>Баланс</b> — <code>{user["balance"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5260687119092817530">🔄</tg-emoji> <b>Оборот</b> — <code>{user["turnover"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258508428212445001">🎮</tg-emoji> <b>Сыграно</b> — <code>{user["win_game"] + user["lose_game"]} игр.</code>\n\n'
        f'<tg-emoji emoji-id="5258336354642697821">⬇️</tg-emoji> <b>Пополнений</b> — <code>{user["amount_replenishment"]:.2f}</code><tg-emoji emoji-id="5116648080787112958">💰</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258043150110301407">⬆️</tg-emoji> <b>Выводов</b> — <code>{user["amount_withdraw"]:.2f}</code><tg-emoji emoji-id="5116648080787112958">💰</tg-emoji>\n'
        f'<tg-emoji emoji-id="5260221883940347555">🔫</tg-emoji> <b>Макс. вин</b> — <code>{user["max_win"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>'
    )
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, text, parse_mode='HTML', reply_markup=start_statistick_keyboard())

@router.message(F.text.casefold().in_(["стата", "статистика", "/статистика", "stats"]))
async def message_statistick_start(message: Message):
    user = await db.users.get_user(message.from_user.id)
    text = (
        f'<blockquote><tg-emoji emoji-id="5258330865674494479">🍑</tg-emoji> <b>Статистика</b> @{message.from_user.username}</blockquote>\n\n'
        f'<tg-emoji emoji-id="5258204546391351475">💰</tg-emoji> <b>Баланс</b> — <code>{user["balance"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5260687119092817530">🔄</tg-emoji> <b>Оборот</b> — <code>{user["turnover"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258508428212445001">🎮</tg-emoji> <b>Сыграно</b> — <code>{user["win_game"] + user["lose_game"]} игр.</code>\n\n'
        f'<tg-emoji emoji-id="5258336354642697821">⬇️</tg-emoji> <b>Пополнений</b> — <code>{user["amount_replenishment"]:.2f}</code><tg-emoji emoji-id="5116648080787112958">💰</tg-emoji>\n'
        f'<tg-emoji emoji-id="5258043150110301407">⬆️</tg-emoji> <b>Выводов</b> — <code>{user["amount_withdraw"]:.2f}</code><tg-emoji emoji-id="5116648080787112958">💰</tg-emoji>\n'
        f'<tg-emoji emoji-id="5260221883940347555">🔫</tg-emoji> <b>Макс. вин</b> — <code>{user["max_win"]:.2f}</code><tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>'
    )
    await message.answer(text, parse_mode='HTML')
