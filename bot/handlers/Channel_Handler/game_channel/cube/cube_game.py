# main
from data.config import db, channel_game_id

from handlers.Channel_Handler.game_channel.lose_function import payout_lose
from handlers.Channel_Handler.game_channel.win_function import payout_winnings
from handlers.Channel_Handler.game_channel.cube.cube_tie import payout_tie_cube
from handlers.Channel_Handler.channel_function import get_game_coefficient

# module 
import asyncio

async def roll_dice(bot, soo, count=1):
    dices = [
        await bot.send_dice(chat_id=channel_game_id, reply_to_message_id=soo)
        for _ in range(count)
    ]
    return [d.dice.value for d in dices]

async def start_game_cubik(stavka, value, user_id, soo, bot):
    two_dice_stavki = {
        'ничья': lambda d1, d2: d1 == d2,
        'победа1': lambda d1, d2: d1 > d2,
        'п1': lambda d1, d2: d1 > d2,
        'победа2': lambda d1, d2: d1 < d2,
        'п2': lambda d1, d2: d1 < d2,
    }
    
    single_dice_stavki = {
        'чёт': [2, 4, 6],
        'чет': [2, 4, 6],
        'нечёт': [1, 3, 5],
        'нечет': [1, 3, 5],
        'больше': [4, 5, 6],
        'меньше': [1, 2, 3],
        '1': [1],
        '2': [2],
        '3': [3],
        '4': [4],
        '5': [5],
        '6': [6],
        'сектор1': [1, 2],
        'сектор 1': [1, 2],
        'сектор2': [3, 4],
        'сектор 2': [3, 4],
        'сектор3': [5, 6],
        'сектор 3': [5, 6],

    }

    two_dice_value = {
        # меньше --
        '2меньше': lambda d1, d2: d1 in [1, 2, 3] and d2 in [1, 2, 3],
        '2м': lambda d1, d2: d1 in [1, 2, 3] and d2 in [1, 2, 3],
        '2 меньше': lambda d1, d2: d1 in [1, 2, 3] and d2 in [1, 2, 3],

        # меньше --
        '2больше': lambda d1, d2: d1 in [4, 5, 6] and d2 in [4, 5, 6],
        '2б': lambda d1, d2: d1 in [4, 5, 6] and d2 in [4, 5, 6],
        '2 больше': lambda d1, d2: d1 in [4, 5, 6] and d2 in [4, 5, 6],

        # чет --
        '2ч': lambda d1, d2: d1 in [4, 2, 6] and d2 in [4, 2, 6],
        '2 чет': lambda d1, d2: d1 in [4, 2, 6] and d2 in [4, 2, 6],
        '2чет': lambda d1, d2: d1 in [4, 2, 6] and d2 in [4, 2, 6],
        '2 чёт': lambda d1, d2: d1 in [4, 2, 6] and d2 in [4, 2, 6],
        '2чёт': lambda d1, d2: d1 in [4, 2, 6] and d2 in [4, 2, 6],

        # нечет --
        '2н': lambda d1, d2: d1 in [1, 3, 5] and d2 in [1, 3, 5],
        '2 нечет': lambda d1, d2: d1 in [1, 3, 5] and d2 in [1, 3, 5],
        '2нечет': lambda d1, d2: d1 in [1, 3, 5] and d2 in [1, 3, 5],
        '2 нечёт': lambda d1, d2: d1 in [1, 3, 5] and d2 in [1, 3, 5],
        '2нечёт': lambda d1, d2: d1 in [1, 3, 5] and d2 in [1, 3, 5],
    } 

    if stavka in single_dice_stavki:
        [value_dice] = await roll_dice(bot, soo, 1)

        await asyncio.sleep(1.2)

        if value_dice in single_dice_stavki[stavka]:
            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)
        else:
            await payout_lose(value, soo, user_id, bot)

    elif stavka in two_dice_stavki:
        value_dice1, value_dice2 = await roll_dice(bot, soo, 2)

        await asyncio.sleep(1.2)

        if two_dice_stavki[stavka](value_dice1, value_dice2):
            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)

        elif stavka != 'ничья' and value_dice1 == value_dice2:
            await payout_tie_cube(value, soo, user_id, bot)

        else:
            await payout_lose(value, soo, user_id, bot)

    elif stavka in two_dice_value:
        value_dice1, value_dice2 = await roll_dice(bot, soo, 2)

        await asyncio.sleep(1.2)

        if two_dice_value[stavka](value_dice1, value_dice2):
            koef = get_game_coefficient(stavka)
            value_win = round(float(value) * koef, 2)
            await payout_winnings(koef, value_win, value, soo, user_id, bot)
        else:
            await payout_lose(value, soo, user_id, bot)