# main
from data.config import db, channel_game_id, url_bot
from aiogram import Bot
from config_reader import config
from utils.help_function import clean
import handlers.Channel_Handler.channel_function as channel_functions
from keyboards.Admin_Keyboards.Logs_Keyboard.logs_keyboard import (
    select_logs_out_ref_bonus,
    ling_game_bot
)

async def logs_succes_deposit(username, first_name, user_id, amount, balance, bot: Bot):
    await bot.send_message(chat_id=config.logs_id,
                           text=clean(f"""
                            <code>[LOG]</code> 💸 New <b>deposit</b>

                            👤 Игрок: <b>{first_name} (@{username} - <code>{user_id}</code>)</b>
                            💰 <b>Пополнил</b> баланс на сумму <b>{amount}$</b>
                            🦋 Баланс игрока: <b>{balance}$</b>
                            
                            <b>🐼 Просто пандочка для настроения</b>"""),
                            message_thread_id=config.topic_deposit)
    
async def logs_succes_withdraw(username, first_name, user_id, amount, balance, bot: Bot):
    await bot.send_message(chat_id=config.logs_id,
                           text=clean(f"""
                            <code>[LOG]</code> 💰 New <b>withdraw</b>

                            👤 Игрок: <b>{first_name} (@{username} - <code>{user_id}</code>)</b>
                            💰 <b>Вывел:</b> <b>{amount}$</b>
                            🦋 Баланс игрока: <b>{balance}$</b>
                            
                            <b>🐸 Просто лягушка для настроения</b>"""),
                            message_thread_id=config.topic_withdraw)
    
async def logs_out_referal_bonus(username, first_name, user_id, amount, refs_paid_now, bot: Bot):
    
    total_refs = await db.referals.count_referals(user_id)
    turnover = await db.referals.get_referal_turnover_bonus(user_id)

    await bot.send_message(
        chat_id=config.logs_id,
        text=clean(f"""
        <code>[LOG]</code> 🎁 Новая заявка на <b>выплату реферального бонуса</b>

        👤 Игрок: <b>{first_name} (@{username or '—'} - <code>{user_id}</code>)</b>
        💰 Хочет вывести: <b>{amount}$</b>
        🫂 Всего рефералов: <b>{total_refs} чел.</b>
        💸 Всего заработано: <b>{turnover}$</b>
        👀 Выплата за: <b>{refs_paid_now} чел.</b>

        <b>🐥 Просто цыпа для настроения</b>"""),
        reply_markup=select_logs_out_ref_bonus(user_id, amount),
        message_thread_id=config.topic_ref_bonus
    )

async def logs_create_mines_game(user_id, username, first_name, count_mines, amount, bot: Bot):

    soo, _, final_name, value = await channel_functions.check_reklama_user(first_name, "мины", amount, user_id, bot, True)
    await bot.send_message(chat_id=channel_game_id,
                           text=f"<b>{final_name}</b> — запустил игру 💣 Мины в нашем <b><a href='{url_bot}'>боте</a></b>",
                           reply_markup=ling_game_bot(),
                           reply_to_message_id=soo,
                           disable_web_page_preview=True)
    
    await bot.send_message(chat_id=config.logs_id,
                           text=clean(f"""
                            <code>[LOG]</code> 💣 New <b>mines game</b>

                            👤 Игрок: <b>{first_name} (@{username} - <code>{user_id}</code>)</b>
                            💰 <b>Ставка:</b> <b>{value}$</b>
                            💣 Мин: <b>{count_mines} шт.</b>
                            🦋 Осталось: <b>{await db.users.get_balance(user_id)}$</b>
                            
                            <b>🧨 Просто динамит для настроения</b>"""))
    
    return value