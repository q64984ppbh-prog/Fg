from data.config import db, channel_game_id
from handlers.Channel_Handler.game_channel.cube.cube_game import start_game_cubik
from handlers.Channel_Handler.game_channel.basketball.start_basketball import start_game_basket
from handlers.Channel_Handler.game_channel.darts.darts_game import start_game_darts
from handlers.Channel_Handler.game_channel.slot.slot_game import start_game_slot
from handlers.Channel_Handler.game_channel.plinko.start_plinko import start_game_plinko
from handlers.Channel_Handler.game_channel.bouling.bouling_game import start_game_boul
from handlers.Channel_Handler.game_channel.rock.start_rock import start_game_rock
from handlers.Channel_Handler.game_channel.football.start_football import start_football_game
from keyboards.Channel_Keyboards.channel_key import keyboard_in_game_message
import asyncio

async def start_game_channel_is_ochered(stavka, value, user_id_channel, soo, bot):
    if stavka in ['чёт', 'чет', 'нечёт', 'нечет',
                      'больше', 'меньше', 'ничья', '1', '2', '3', '4', '5', '6',
                      'ничья','победа1', 'п1', 'победа2', 'п2', 'победа 1', 'победа 2',
                      '2м', '2меньше', '2 меньше',
                      '2б', '2больше', '2 больше',
                      '2ч', '2 чет', '2чет', '2 чёт', '2чёт',
                      '2н', '2 нечет', '2нечет', '2 нечёт','2нечёт', 
                      'сектор1', 'сектор 1', 'сектор2', 'сектор 2', 'сектор3', 'сектор 3']:
            await start_game_cubik(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['красное', 'красн', 
                      'белое', 'бел', 'центр', 'яблочко', 'дартс центр', 'дартс яблочко',
                      'дартс промах', 'дартс мимо', 'дарц промах', 'дарц мимо',
                      'дартс дуэль', 'Дартс дуэль']:
            await start_game_darts(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['слоты', 'казик']:
            await start_game_slot(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['баскет гол', 'баскет попал', 'гол', 'попал',
                        'баскет промах', 'баскет мимо', 'баскетбол гол', 'баскетбол промах']:
            await start_game_basket(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['фут гол', 'футбол гол', 'футбол промах', 'фут промах']:
          await start_football_game(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['пл', 'плинко', 'plinko']:
            await start_game_plinko(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['боул дуэль', 'боулинг дуэль', 'Боул дуэль', 'Боулинг дуэль']:
            await start_game_boul(stavka, value, user_id_channel, soo, bot)
    elif stavka in ['камень', 'ножницы', 'бумага']:
          await start_game_rock(stavka, value, user_id_channel, soo, bot)
    return True


async def process_bet(bet, bot):
    bet_id, name, user_id, value, stavka, message_id = bet[:6]
    source = bet[6] if len(bet) > 6 else 'bot'

    try:
        user_info = await bot.get_chat(user_id)
        full_name = user_info.full_name or name
        first_name = user_info.first_name or ''
        last_name = user_info.last_name or ''
        has_pripiska = '@duckwins' in first_name.lower() or '@duckwins' in last_name.lower()
    except:
        full_name = name
        has_pripiska = False

    payment_text = "🦋 CryptoBot" if source == 'cryptobot' else "🤖 DuckWin"
    
    bonus_text = ""
    actual_value = float(value)
    if has_pripiska:
        bonus = actual_value * 0.026
        actual_value = actual_value + bonus
        bonus_text = "\n🎁 Бонус 2.6% за приписку!"
    
    caption = f"❤️‍🔥 {full_name} поставил на {stavka}\n\n💳 Ставка: {actual_value:.2f}💵\n💎 Лига: 🚀 Rookie\n🧾 Оплата через {payment_text}{bonus_text}"

    sent_msg = await bot.send_message(
        chat_id=channel_game_id,
        text=caption,
        reply_markup=keyboard_in_game_message()
    )

    soo = sent_msg.message_id

    if has_pripiska:
        value = actual_value

    await db.game_channel.update_channel_post_id(bet_id, soo)

    # Обновляем кнопку юзера
    try:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        channel_link = f"https://t.me/c/2514725444/{soo}"
        new_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 Ваша ставка", url=channel_link)],
            [InlineKeyboardButton(text="🔄 Повторить", callback_data="nop")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="create_game")]
        ])
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=message_id + 1,
            reply_markup=new_kb
        )
    except Exception as e:
        pass

    success = await start_game_channel_is_ochered(stavka, value, user_id, soo, bot)
    
    if success:
        await db.game_channel.update_bet_status(bet_id, 'done')
        await db.game_channel.dell_queue(bet_id)
    else:
        await db.game_channel.update_bet_status(bet_id, 'failed')
        await db.game_channel.dell_queue(bet_id)


async def process_bets_in_strict_sequence(db_core, bot):
    print('воркер для ставок запущен')

    while True:
        async with db_core.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("""
                    SELECT id, name, user_id, value, stavka, message_id, COALESCE(source, 'bot') as source
                    FROM channelbet
                    WHERE status = 'pending'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                """)

                if not row:
                    await asyncio.sleep(1.5)
                    continue

                bet_id = row['id']
                name = row['name']
                user_id = row['user_id']
                value = row['value']
                stavka = row['stavka']
                message_id = row['message_id']
                bet_source = row['source'] if row['source'] else 'bot'

                await conn.execute("""
                    UPDATE channelbet
                    SET status = 'in_progress'
                    WHERE id = $1
                """, bet_id)

        bet_tuple = (bet_id, name, user_id, value, stavka, message_id, bet_source)
        await process_bet(bet_tuple, bot)

        await asyncio.sleep(3.5)
