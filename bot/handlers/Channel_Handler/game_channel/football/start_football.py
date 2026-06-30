#bot
from data.config import channel_game_id, db # Конфиги

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.channel_function import get_game_coefficient

#module
from aiogram import types
import asyncio

async def roll_football(bot, soo, count=1):
    dices = [
        await bot.send_dice(
            chat_id=channel_game_id,
            emoji='⚽️',
            reply_to_message_id=soo
        )
        for _ in range(count)
    ]
    return [d.dice.value for d in dices]

async def start_football_game(stavka, value, user_id, soo, bot):
    if stavka in ['фут гол', 'футбол гол']:
        [value_dice] = await roll_football(bot, soo, 1)

        await asyncio.sleep(1.2)

        if value_dice in [3, 4, 5]:

            koef = get_game_coefficient(stavka)
            value_ = float(value) * koef
            value_win = round(value_, 2)

            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        else:
            await payout_lose(value, soo, user_id, bot)
        
    elif stavka in ['футбол промах', 'фут промах']:
        [value_dice] = await roll_football(bot, soo, 1)

        await asyncio.sleep(1.2)

        if value_dice in [1, 2]:

            koef = get_game_coefficient(stavka)
            value_ = float(value) * koef
            value_win = round(value_, 2)

            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        else:
            await payout_lose(value, soo, user_id, bot)