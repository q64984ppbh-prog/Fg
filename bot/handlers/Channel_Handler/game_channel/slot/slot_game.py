# main
from data.config import db, channel_game_id

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings

# module 
import asyncio
from aiogram import types

async def start_game_slot(stavka, value, user_id, soo, bot):
    if stavka in ['слоты', 'казик']:
        await asyncio.sleep(1)
        dice = await bot.send_dice(channel_game_id, emoji='🎰', reply_to_message_id=soo)
        value_dice = dice.dice.value

        if value_dice in [43]:

            await asyncio.sleep(1.2)

            value_ = float(value) * 4
            value_win = round(value_, 2)

            await payout_winnings(4, value_win, value, soo, user_id, bot)

        elif value_dice in [22]:

            await asyncio.sleep(1.2)


            value_ = float(value) * 5
            value_win = round(value_, 2)

            await payout_winnings(5, value_win, value, soo, user_id, bot)

        elif value_dice in [1]:

            await asyncio.sleep(1.2)

            value_ = float(value) * 4
            value_win = round(value_, 2)

            await payout_winnings(4, value_win, value, soo, user_id, bot)

        elif value_dice in [64]:

            await asyncio.sleep(1.2)

            value_ = float(value) * 13
            value_win = round(value_, 2)

            await payout_winnings(13, value_win, value, soo, user_id, bot)

        else:
            
            await asyncio.sleep(1.2)
            await payout_lose(value, soo, user_id, bot)