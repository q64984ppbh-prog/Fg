# main
from data.config import db, channel_game_id

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.game_channel.darts.darts_tie import payout_tie_darts
from handlers.Channel_Handler.channel_function import get_game_coefficient

# module 
import asyncio
from aiogram import types

async def roll_darts(bot, soo, count=1):
    dices = [
        await bot.send_dice(
            chat_id=channel_game_id,
            emoji='🎯',
            reply_to_message_id=soo
        )
        for _ in range(count)
    ]
    return [d.dice.value for d in dices]

async def start_game_darts(stavka, value, user_id, soo, bot):
    single_dice_stavki = {
        'красное': [2, 4],
        'красн': [2, 4],
        'белое': [3, 5],
        'бел': [3, 5],
        'центр': [6],
        'яблочко': [6], 
        'дартс центр': [6], 
        'дартс яблочко': [6],
        'дартс промах': [1], 
        'дартс мимо': [1], 
        'дарц промах': [1], 
        'дарц мимо': [1],
    }

    if stavka in single_dice_stavki:
        [value_dice] = await roll_darts(bot, soo, 1)
        
        await asyncio.sleep(1.2)

        if value_dice in single_dice_stavki[stavka]:

            koef = get_game_coefficient(stavka)
            value_ = float(value) * koef
            value_win = round(value_, 2)
            
            await payout_winnings(koef, value_win, value, soo, user_id, bot)
        else:

            await payout_lose(value, soo, user_id, bot)

    elif stavka in ["дартс дуэль", "Дартс дуэль"]:
        value_dice1, value_dice2 = await roll_darts(bot, soo, 2)
        
        await asyncio.sleep(1.2)

        if value_dice1 > value_dice2:

            koef = get_game_coefficient(stavka)
            value_ = float(value) * koef
            value_win = round(value_, 2)
                
            await payout_winnings(koef, value_win, value, soo, user_id, bot)
            
        elif value_dice1 < value_dice2:
                await payout_lose(value, soo, user_id, bot)

        else:
            await payout_tie_darts(value, soo, user_id, bot)
