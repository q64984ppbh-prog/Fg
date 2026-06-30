# main
import re
import asyncio
from aiogram import F, Router
from aiogram.types import Message

# other
from data.config import logs_channel_id, db
import handlers.Channel_Handler.channel_function as channel_functions
from utils.function_bot import check_registration

router = Router()
@router.channel_post(F.chat.id == logs_channel_id)
async def handler_channelpost(message: Message):

    entata = message.entities
    bot = message.bot

    if await channel_functions.get_user_id_entata(bot, entata):
        user_id_channel = entata[0].user.id
        name = entata[0].user.first_name
        username = entata[0].user.username
        comment = message.text.split('💬 ')
        start_command = ''

        await check_registration(username, user_id_channel, name, start_command, bot)
        if await channel_functions.check_abuz_name(name, message):
            stavka = await channel_functions.get_stavka(comment)
            match = re.search(r'отправил\(а\).*?\(\$(.+?)\)', message.text)
            values = await channel_functions.get_amount(match)

            soo, valid, final_name, value = await channel_functions.check_reklama_user(name, stavka, values, user_id_channel, bot)
            await asyncio.sleep(1.5)
            if valid:
                if await channel_functions.handle_invalid_bet(stavka, value, soo, user_id_channel, final_name, bot):
                    bet_id = await db.game_channel.add_bet_to_queue(final_name, user_id_channel, value, stavka, soo, source="cryptobot")
                    await db.users.add_turnover(user_id_channel, value)
                    await db.users.add_replenishment(user_id=user_id_channel, amount=value)
                    await channel_functions.check_user_level_up(user_id_channel, bot)