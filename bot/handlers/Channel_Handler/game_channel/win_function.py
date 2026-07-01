from aiogram import Bot
from aiogram.types import FSInputFile
from utils.help_function import clean
from data.config import db, channel_game_id
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message
import asyncio

def build_text(koef, value_win):
    premium_text = clean(f"""<emoji id='5224257782013769471'>💰</emoji> <u><b>Вы выиграли!</b></u>
                         
<blockquote><b><emoji id='5436386989857320953'>🤑</emoji> На ваш баланс было
зачислено {value_win}<emoji id='5409048419211682843'>💵</emoji> (x{koef})
Опробуй свою удачу вновь!</b></blockquote>""")

    no_prem_text = clean(f"""☘️ <u><b>Вы выиграли!</b></u>
                         
<blockquote><b>💸 На ваш баланс было
зачислено {value_win}$ (x{koef})
💰 Опробуй свою удачу вновь!</b></blockquote>""")
    return premium_text, no_prem_text

async def payout_winnings(koef, value_win, value, soo, user_id, bot: Bot):
    animation = FSInputFile('animation/win.mp4')
    premium_text, no_premium_text = build_text(koef, value_win)
    
    try:
        await bot.send_animation(
            chat_id=channel_game_id,
            animation=animation,
            caption=no_premium_text,
            reply_to_message_id=soo,
            reply_markup=keyboard_in_game_message()
        )
    except Exception as outer_e:
        await bot.send_message(6255869883, f"{outer_e}")
    
    try:
        await db.users.add_balance(user_id, value_win)
        await bot.send_message(chat_id=user_id, text=f"<tg-emoji emoji-id=\"5472363448404809929\">👛</tg-emoji> Зачислено {value_win:.2f}<tg-emoji emoji-id=\"5409048419211682843\">💵</tg-emoji>")
    except Exception as e:
        await bot.send_message(6255869883, f"Ошибка начисления: {e}")
