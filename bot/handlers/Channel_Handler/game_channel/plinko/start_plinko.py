# main
from data.config import db, channel_game_id

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.game_channel.cube.cube_tie import payout_tie_cube

# module 
import asyncio
from aiogram import types

async def roll_dice(bot, soo, emoji='🎲', count=1):
    dices = [
        await bot.send_dice(chat_id=channel_game_id, emoji=emoji, reply_to_message_id=soo)
        for _ in range(count)
    ]
    return [d.dice.value for d in dices]

async def start_game_plinko(stavka, value, user_id, soo, bot):
    if stavka in ['пл', 'плинко', 'plinko']:

        [dice_value] = await roll_dice(bot, soo, emoji='🎲', count=1)
        await asyncio.sleep(1.2)

        if dice_value == 1:
            await payout_lose(value, soo, user_id, bot)

        elif dice_value == 2:
            value_win = round(float(value) * 0.3, 2)
            await payout_winnings(0.3, value_win, value, soo, user_id, bot)

        elif dice_value == 3:
            value_win = round(float(value) * 0.6, 2)
            await payout_winnings(0.6, value_win, value, soo, user_id, bot)

        elif dice_value == 4:
            value_win = round(float(value) * 1.3, 2)
            await payout_winnings(1.3, value_win, value, soo, user_id, bot)

        elif dice_value == 5:
            value_win = round(float(value) * 1.45, 2)
            await payout_winnings(1.45, value_win, value, soo, user_id, bot)

        elif dice_value == 6:
            value_win = round(float(value) * 1.7, 2)
            await payout_winnings(1.7, value_win, value, soo, user_id, bot)