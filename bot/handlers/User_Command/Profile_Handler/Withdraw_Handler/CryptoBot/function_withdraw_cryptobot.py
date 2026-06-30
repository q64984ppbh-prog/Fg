# main
from utils.help_function import clean
from data.config import db, url_check_group, check_group
import data.config as cfg
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import activated_check_user_keyboard, activated_error_keyboard

# Other
import re
import asyncio
import random
from pyrogram.raw import functions
from pyrogram.types import InlineKeyboardMarkup

async def send_command(amount, user_id, url, chat_id, username):

    if not cfg.check_client.is_connected:
        await cfg.check_client.start()

    bot_username = '@send'

    try:
        chat_info = await cfg.check_client.get_chat(url)
        chat_id = chat_info.id
    except Exception as e:
        return

    query_result = await cfg.check_client.invoke(
        functions.messages.GetInlineBotResults(
            bot=await cfg.check_client.resolve_peer(bot_username),
            peer=await cfg.check_client.resolve_peer(chat_id),
            query=f"{amount}",
            offset=""
        )
    )

    await asyncio.sleep(1.5)
    if query_result.results:
        query_id = query_result.query_id

        for result in query_result.results:
            if f"Отправить" in result.title:

                if hasattr(result, 'send_message') and hasattr(result.send_message, 'reply_markup'):
                    buttons = result.send_message.reply_markup.rows
                    for row in buttons:
                        for button in row.buttons:
                            if button.text == "…":
                                random_id = random.randint(0, 2**63 - 1)
                                await cfg.check_client.invoke(
                                    functions.messages.SendInlineBotResult(
                                        peer=await cfg.check_client.resolve_peer(chat_id),
                                        query_id=query_id,
                                        id=result.id,
                                        random_id=random_id,
                                        hide_via=True
                                    )
                                )
                                await asyncio.sleep(3)
                                async for message in cfg.check_client.get_chat_history(chat_id, limit=1):
                                    if message.reply_markup and isinstance(message.reply_markup, InlineKeyboardMarkup):

                                        for row in message.reply_markup.inline_keyboard:
                                            for button in row:
                                                if button.url:
                                                    await asyncio.sleep(2)
                                                    command = clean(f"""
                                                    <b>👤 @{username}</b> 
                                                    <b>👉🏻 <code>{user_id}</code></b>
                                                    <b>💸 <code>{amount}$</code></b>""")
                                                    await cfg.check_client.send_message(chat_id=chat_id, text=command, reply_to_message_id=message.id)
                                                    return button.url
                                                else:
                                                    return None
                break
        else:
            await asyncio.sleep(2)
            command = clean(f"""
            <b>👤 @{username}</b> 
            <b>👉🏻 <code>{user_id}</code></b>
            <b>💸 <code>{amount} USDT</code>
            <code>♨️ Error</code>
            ℹ️ Нет нужной кнопки</b>""")

            await cfg.check_client.send_message(chat_id=chat_id, text=command)
            return None
    else:
        await asyncio.sleep(2)
        command = clean(f"""
            <b>👤 @{username}</b> 
            <b>👉🏻 <code>{user_id}</code></b>
            <b>💸 <code>{amount} USDT</code>
            <code>♨️ Error</code>
            ℹ️ Нет результатов для отправки</b>""")

        await cfg.check_client.send_message(chat_id=chat_id, text=command)
        return None
    


async def process_out_bet(out_bet, bot):
    out_id, amount, user_id, username, status = out_bet

    try:

        await db.send.update_check_status(out_id, 'in_progress')
        out_wallet = await send_command(amount, user_id, url_check_group, check_group, username)

        if out_wallet is None:
            await db.users.add_balance(user_id, amount)
            await bot.send_message(
                chat_id=user_id,
                caption=clean(f"""
                            <i>❌ Произошла ошибка.</i>
                              
                            • <code>USDT зачислены обратно</code>
                            • <code>Попробуйте чуть позже</code>"""),
                reply_markup=activated_error_keyboard()
            )
            await db.send.update_check_status(out_id, 'failed')
        else:
            link_pattern = r'(http://t.me/send\?start=[\w-]+)'
            link_match = re.search(link_pattern, out_wallet)
            if link_match:
                link = link_match.group(0)
                await bot.send_message(
                    chat_id=user_id,
                    caption=(
                        f"<b>💸 Ваш чек на сумму <code>{amount}$</code></b>"
                    ),
                    reply_markup=activated_check_user_keyboard(link, amount)
                )
                await db.send.update_check_status(out_id, 'done')
            else:
                await db.plus_balance(amount, user_id)
                await bot.send_message(
                    chat_id=user_id,
                    caption=clean(f"""
                            <i>❌ Произошла ошибка.</i>
                              
                            • <code>USDT зачислены обратно</code>
                            • <code>Попробуйте чуть позже</code>"""),
                    reply_markup=activated_error_keyboard()
                            )
                await db.send.update_check_status(out_id, 'failed')
        await db.send.dell_check(out_id)

    except Exception as e:
        await db.send.update_check_status(out_id, 'failed')
        await db.send.dell_check(out_id)


async def process_outs_in_sequence(db_core, bot):
    while True:
        async with db_core.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("""
                    SELECT id, amount, user_id, username, status
                    FROM out_queue
                    WHERE status = 'pending'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """)

                if not row:
                    await asyncio.sleep(2.5)
                    continue

                out_id = row['id']
                amount = float(row['amount'])
                user_id = row['user_id']
                username = row['username']
                status = row['status']

                await conn.execute("""
                    UPDATE out_queue
                    SET status = 'in_progress'
                    WHERE id = $1
                """, out_id)

        out_bet_tuple = (out_id, amount, user_id, username, status)
        await process_out_bet(out_bet_tuple, bot)
        await asyncio.sleep(0.3)