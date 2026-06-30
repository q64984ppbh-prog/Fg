#bot
from data.config import channel_game_id, db # Конфиги

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.channel_function import get_game_coefficient

#module
from aiogram import types
import asyncio

async def roll_basket(bot, soo):
    dice = await bot.send_dice(
        chat_id=channel_game_id,
        emoji='🏀',
        reply_to_message_id=soo
    )
    return dice.dice.value

async def start_game_basket(stavka, value, user_id, soo, bot):
    if stavka in ['баскет промах', 'баскет мимо', 'баскетбол промах', 'баскетбол мимо']:
        value_dice = await roll_basket(bot, soo)

        await asyncio.sleep(1.2)

        if value_dice not in [4, 5]:
            
            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)

            await payout_winnings(koef, value_win, value, soo, user_id, bot)
        else:
            await payout_lose(value, soo, user_id, bot)

    elif stavka in ['баскет гол', 'баскет попал', 'гол', 'попал', 'баскетбол гол', 'баскетбол попал']:
        value_dice = await roll_basket(bot, soo)

        await asyncio.sleep(1.2)
        if value_dice in [4, 5]:

            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)

            await payout_winnings(koef, value_win, value, soo, user_id, bot)
        else:
            await payout_lose(value, soo, user_id, bot)