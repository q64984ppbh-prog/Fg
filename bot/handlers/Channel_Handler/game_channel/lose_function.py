# main
from aiogram import F, Router
from aiogram.types import FSInputFile

import os
import data.config as cfg
from utils.help_function import clean
from data.config import db, channel_game_id, url_support_make_bet, url_chat_game
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message
from handlers.Channel_Handler.channel_function import check_referal_balance_turnover


# module 
import asyncio

def build_text():
    premium_text = clean(f"""
    <b><emoji id='5240241223632954241'>🚫</emoji> <u>Вы проиграли..</u>
                         
    <blockquote><emoji id='5217467090826441505'>😡</emoji> Не расстраивайтесь! Удача обязательно улыбнется вам! <emoji id='5429518319243775957'>📉</emoji></blockquote></b>
    
    <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")

    no_prem_text =  clean(f"""
    <b>🚫 <u>Вы проиграли..</u>
                         
    <blockquote>😡 Не расстраивайтесь! Удача обязательно улыбнется вам! 📉</blockquote></b>
    
    <blockquote><b><a href='{url_support_make_bet}'>Как сделать ставку?</a>  • <a href='{url_chat_game}'>Чат</a></b></blockquote>""")

    return premium_text, no_prem_text

async def payout_lose(value, soo, user_id, bot):

    animation = FSInputFile('animation/lose.MP4')
    premium_text, no_premium_text = build_text()

    try:
        messages = await cfg.pyro_client.send_animation(
            chat_id=channel_game_id,
            animation='animation/lose.MP4',
            caption=premium_text,
            reply_to_message_id=soo
        )
    except Exception as outer_e:
        await bot.send_message(6255869883, f"{outer_e}")
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
    
    await db.admin.plus_admin_profit(value)
    await db.users.add_lose_game(user_id)
    await check_referal_balance_turnover(user_id, value, bot)
