#bot
from data.config import channel_game_id, db # Конфиги

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.game_channel.bouling.bouling_tie import payout_tie_boul
from handlers.Channel_Handler.channel_function import get_game_coefficient

#module
from aiogram import types
import asyncio

async def roll_bowling(bot, soo, count=1):
    dices = [
        await bot.send_dice(
            chat_id=channel_game_id,
            emoji='🎳',
            reply_to_message_id=soo
        )
        for _ in range(count)
    ]
    return [d.dice.value for d in dices]

async def start_game_boul(stavka, value, user_id, soo, bot):

    value_dice, value_dice_bot = await roll_bowling(bot, soo, 2)
    await asyncio.sleep(1)

    if value_dice > value_dice_bot:
        koef = get_game_coefficient(stavka)
        value_win = round(float(value) * koef, 2)

        await payout_winnings(koef, value_win, value, soo, user_id, bot)

    elif value_dice < value_dice_bot:
        await payout_lose(value, soo, user_id, bot)

    else:
        await payout_tie_boul(value, soo, user_id, bot)