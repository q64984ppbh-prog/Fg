from aiogram import Bot
from aiogram.types import FSInputFile
from utils.help_function import clean
from data.config import db, channel_game_id
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message
import asyncio

def build_lose_text(value):
    premium_text = clean(f"""<emoji id='5215578414621729980'>🚫</emoji> <u><b>Вы проиграли..</b></u>
                         
<blockquote><b>😡 Не расстраивайтесь! Удача обязательно улыбнется вам!</b></blockquote>""")

    no_prem_text = clean(f"""🚫 <u><b>Вы проиграли..</b></u>
                         
<blockquote><b>😡 Не расстраивайтесь! Удача обязательно улыбнется вам!</b></blockquote>""")
    return premium_text, no_prem_text

async def payout_lose(value, soo, user_id, bot: Bot):
    animation = FSInputFile('animation/lose.MP4')
    premium_text, no_premium_text = build_lose_text(value)
    
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
