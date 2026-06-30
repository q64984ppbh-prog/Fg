# main
from aiogram import F, Router, Bot
from aiogram.types import FSInputFile

import uuid
from utils.help_function import clean
from data.config import db, channel_game_id, url_support_make_bet, url_chat_game, client
import data.config as cfg
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message


# module 
import asyncio

def build_text(koef, value_win):
    premium_text = clean(f"""
    <emoji id='5224257782013769471'>💰</emoji> <u><b>Вы выиграли!</b></u>
                         
    <blockquote><b><emoji id='5436386989857320953'>🤑</emoji> На ваш баланс было
    зачислено {value_win}<emoji id='5409048419211682843'>💵</emoji> (x{koef})
    Опробуй свою удачу вновь!</b></blockquote>
    
    <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")

    no_prem_text =  clean(f"""
    ☘️ <u><b>Вы выиграли!</b></u>
                         
    <blockquote><b>💸 На ваш баланс было
    зачислено {value_win}$ (x{koef})
    💰 Опробуй свою удачу вновь!</b></blockquote>
    
    <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")

    return premium_text, no_prem_text

async def payout_winnings(koef, value_win, value, soo, user_id, bot: Bot):

    animation = FSInputFile('animation/win.mp4')
    premium_text, no_premium_text = build_text(koef, value_win)
    
    # Начисляем выигрыш ДО анимации
    try:
        await db.users.add_balance(user_id, value_win)
        await bot.send_message(chat_id=user_id,
                               caption=f"💰 На ваш баланс зачислено <b>{value_win}$</b>")
    except Exception as balance_e:
        await bot.send_message(6255869883, f"Ошибка начисления: {balance_e}")

    try:
        messages = await cfg.pyro_client.send_animation(
            chat_id=channel_game_id,
            animation='animation/win.mp4',
            caption=premium_text,
            reply_to_message_id=soo
        )
    except Exception as outer_e:
        await bot.send_animation(
            chat_id=channel_game_id,
            animation=animation,
            caption=no_premium_text,
            reply_to_message_id=soo,
            reply_markup=keyboard_in_game_message()
        )
        return

    try:
        await bot.edit_message_reply_markup(
            chat_id=channel_game_id,
            message_id=messages.id,
            reply_markup=keyboard_in_game_message()
        )
    except Exception as inner_e:
        await bot.send_message(6255869883, f"{inner_e}")
    except:
        pass

    profit_minus = float(value_win) - float(value) # Сколько мы потеряли с WIN!
    await db.admin.minus_admin_profit(profit_minus) # Отнимаем профит
    await db.users.add_win_game(user_id) # Добавляем WIN игру
    await db.users.update_max_win(user_id, value_win) # Ставим макс вин челу