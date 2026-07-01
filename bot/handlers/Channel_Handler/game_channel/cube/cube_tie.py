# main
from aiogram import F, Router

import data.config as cfg
from utils.help_function import clean
from data.config import db, channel_game_id, url_support_make_bet, url_chat_game
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message



# module
import asyncio
from aiogram.types import FSInputFile

def build_text(koma):
    premium_text = clean(f"""
        <b><emoji id='5017470156276761427'>🔄</emoji> <u>Ничья! Ставка возвращена.</u></b>
                         
        <blockquote><b><emoji id='5444856076954520455'>🧾</emoji> С учетом комиссии <code>10%</code>
        зачислено {koma}<emoji id='5409048419211682843'>💵</emoji>
        <emoji id='5400362079783770689'>🐳</emoji> Это шанс сделать еще одну ставку!</b></blockquote>
    
        <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")
    no_premium_text = clean(f"""
    <b>🔄 <u>Ничья! Ставка возвращена.</u></b>
                         
    <blockquote><b>🧾 С учетом комиссии <code>10%</code> зачислено {koma}$
    🐳 Это шанс сделать еще одну ставку!</b></blockquote>
    
    <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")
    return premium_text, no_premium_text

async def payout_tie_cube(value, soo, user_id, bot):
    
    koma = float(value) * 0.9 # Забираем 10%
    koma_round = round(koma, 2) # Выдаем процент
    profit = float(value) - float(koma_round) # Наш профит

    premium_text, no_premium_text = build_text(koma_round)
    animation = FSInputFile("animation/win.mp4")

    await asyncio.sleep(0.9)

    try:
        messages = await cfg.pyro_client.send_animation(
                chat_id=channel_game_id,
                animation='animation/win.mp4',
                text=premium_text,
                reply_to_message_id=soo
        )
        try:
            await bot.edit_message_reply_markup(
                chat_id=channel_game_id,
                message_id=messages.id,
                reply_markup=keyboard_in_game_message()
            )
        except Exception as inner_e:
            pass

    except Exception as outer_e:
        await bot.send_animation(
            chat_id=channel_game_id,
            animation=animation,
            text=no_premium_text,
            reply_to_message_id=soo,
            reply_markup=keyboard_in_game_message()
        )
    
    await db.users.add_balance(user_id, koma_round) # Начисляем кешбек в бота
    await db.admin.plus_admin_profit(profit) # Начисляем профит