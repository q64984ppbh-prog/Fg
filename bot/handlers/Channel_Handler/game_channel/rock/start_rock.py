# main
from data.config import db, channel_game_id

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.game_channel.rock.tie_rock import payout_tie_rock
from handlers.Channel_Handler.channel_function import get_game_coefficient

# module 
import random
import asyncio
from aiogram import types

async def roll_rock_paper_scissors(bot, soo, emoji):

    await bot.send_message(channel_game_id, emoji, reply_to_message_id=soo)
    await asyncio.sleep(1.4)

    random_emoji = random.choice(['✊🏻', '✌🏻', '🖐🏻'])
    await bot.send_message(channel_game_id, f'{random_emoji}', reply_to_message_id=soo)

    return random_emoji

async def start_game_rock(stavka, value, user_id, soo, bot):
    if stavka in ['камень']:

        random_emoji = await roll_rock_paper_scissors(bot, soo, '✊🏻')
        await asyncio.sleep(1.2)

        if random_emoji == '✌🏻':

            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        elif random_emoji == '🖐🏻':
            await payout_lose(value, soo, user_id, bot)

        else:
            await payout_tie_rock(value, soo, user_id, bot)

    elif stavka in ['ножницы']:

        random_emoji = await roll_rock_paper_scissors(bot, soo, '✌🏻')
        await asyncio.sleep(1.2)

        if random_emoji == '🖐🏻':

            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        elif random_emoji == '✊🏻':
            await payout_lose(value, soo, user_id, bot)

        else:
            await payout_tie_rock(value, soo, user_id, bot)

    elif stavka in ['бумага']:

        random_emoji = await roll_rock_paper_scissors(bot, soo, '🖐🏻')
        await asyncio.sleep(1.2)

        if random_emoji == '✊🏻':

            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        elif random_emoji == '✌🏻':
            await payout_lose(value, soo, user_id, bot)

        else:
            await payout_tie_rock(value, soo, user_id, bot)