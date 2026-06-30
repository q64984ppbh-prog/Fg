# main
from aiogram import F, Router, Bot
from decimal import Decimal, ROUND_DOWN

# other
import re
import random
import asyncio
import data.config as cfg
from data.configure import GAME_COEFFICIENTS
from data.config import channel_game_id, url_support, db, url_bot
from utils.help_function import clean
from keyboards.Channel_Keyboards.channel_key import keyboard_error_user_id
from data.invalid_channel import invalid_characters, invalid_stavki


async def get_user_id_entata(bot: Bot, entata):
    try:
        cb_winid = entata[0].user.id
        return True
    except Exception:

        try:
            text_prem = clean(f"""
                <b><emoji id="5017088445353296841">🔎</emoji> Бот заметил ошибку!

                <blockquote><emoji id="5341715473882955310">⚙️</emoji> Настройки → Конфиденциальность → Пересылка сообщений → Все.</blockquote>

                <emoji id="5017108172138087141">⚙️</emoji> Для возврата средств свяжитесь с <a href={url_support}>тех.поддержкой</a></b>""")

            await cfg.pyro_client.send_message(
                chat_id=channel_game_id,
                disable_web_page_preview=True,
                caption=text_prem
            )
        except:
            text = clean(f"""
                <b>🔎 Бот заметил ошибку!

                <blockquote>⚙️ Настройки → Конфиденциальность → Пересылка сообщений → Все.</blockquote>

                ⚙️ Для возврата средств свяжитесь с <a href={url_support}>тех.поддержкой</a></b>""")

            await bot.send_message(
                chat_id=channel_game_id,
                caption=text,
                disable_web_page_preview=True,
                reply_markup=keyboard_error_user_id()
            )

        return False
    

async def check_abuz_name(name, message):
    if 'отправил(а)' in name:
                text = clean(f"""
               <b>[<emoji id="5420323339723881652">⚠️</emoji>] Бот заметил попытку абуза!</b>
                                            
                <blockquote><b>• Бот не засчитает ставку!
                • Средства будут не засчитаны!</b></blockquote>""")

                await cfg.pyro_client.send_message(
                    chat_id=channel_game_id,
                    caption=text,
                    reply_markup=keyboard_error_user_id()
                )
                return False
    else:
        return True
    
async def get_stavka(comment):
    try:
        comment_data = comment[1]
    except:
        comment_data = comment[0]

    st = comment_data.replace('💬', '')
    stavka = st.lower()
    return stavka

async def get_amount(match):
    value_str = match.group(1).replace(',', "").strip()
    try:
        value_ = float(value_str)
        value = round(value_, 2)
        return value
    except ValueError:
        return None

async def clean_name(name, user_id, allowed_tag="duckwins"):
    words = name.split()
    filtered_words = []
    allowed_parts = []

    is_anon = await db.users.get_anonimnost(user_id)
    if is_anon:
        return "Игрок"

    for word in words:
        if word.startswith('@'):
            tag = word[1:].lower()
            if tag == allowed_tag:
                allowed_parts.append(word)
        else:
            filtered_words.append(word)

    new_name = ' '.join(filtered_words).strip()
    for invalid in invalid_characters:
        pattern = re.compile(re.escape(invalid), re.IGNORECASE)
        new_name = pattern.sub('', new_name)
    
    new_name = ' '.join(new_name.split())
    
    if allowed_parts:
        new_name = f"{new_name} {' '.join(allowed_parts)}".strip()

    return new_name

async def get_bonus(user_id, value, name):
    is_anon = await db.users.get_anonimnost(user_id)
    bonus_percent = Decimal('0')

    if is_anon:
        return bonus_percent, value

    actual_percent_flag = await db.admin.get_value('Flag_Bonus_Pripiska')
    if actual_percent_flag != 1:
        return bonus_percent, value

    name_words = name.split()
    has_pripiska = any(word.lower() == "@duckwins" for word in name_words)

    if not has_pripiska:
        return bonus_percent, value

    bonus_percent = Decimal(str(random.randint(0, 100) / 10))

    if bonus_percent > 0:
        value = Decimal(value)
        value += (value * bonus_percent / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    return bonus_percent, value

async def build_text(new_name, stavka, value, level, bonus_percent, stavka_bot):
    extra_text = ""
    extra_prem_text = ""
    if bonus_percent > 0:
        extra_text = f"🎁 Бонус <code>{bonus_percent:.1f}%</code> за приписку!"
        extra_prem_text = f"<emoji id='5226731292334235524'>🎁</emoji> Бонус <code>{bonus_percent:.1f}%</code> за приписку!"

    send_link = "https://t.me/send"
    duck_stavki = ['мины']

    if stavka_bot or stavka in duck_stavki:

        text_payment = f"🧾 Оплата через <b><a href='{url_bot}'>🤖 Duck Bot</a></b>"
        prem_payment = f"🧾 Оплата через <b><emoji id='5372981976804366741'>🤖</emoji><a href='{url_bot}'>Duck Bot</a></b>"
    else:
        text_payment = f"🧾 Оплата через <b><a href='{send_link}'>🦋 CryptoBot</a></b>"
        prem_payment = f"🧾 Оплата через <b><emoji id='5361836987642815474'>🦋</emoji><a href='{send_link}'>CryptoBot</a></b>"

    text = clean(f"""
        🎲 <b>{new_name}</b> поставил на <b>{stavka}</b>
        
        <blockquote>💳 Ставка: <b>{value:.2f}$</b>
        💎 Лига: <b>{level}</b>
        {text_payment}
        {extra_text}</blockquote>""")

    text_prem_emoji = clean(f"""
        <emoji id="5224427772524376976">❤️‍🔥</emoji> <b>{new_name}</b> поставил на <b>{stavka}</b>

        <blockquote><emoji id='5445353829304387411'>💳</emoji> Ставка: <b>{value:.2f}<emoji id='5409048419211682843'>💵</emoji></b>
        <emoji id='5235630047959727475'>💎</emoji> Лига: <b>{level}</b>
        {prem_payment}
        {extra_prem_text}</blockquote>""")

    return text, text_prem_emoji

async def build_max_dep_text(new_name, koma):

    text = clean(f"""
        <b>🚫 <u>{new_name}</u> вы поставили слишком большую ставку!

        <blockquote>• Максимальная ставка: {await db.admin.get_value('Max_Dep')}$
        • Бот вернет вам: {koma}$</blockquote></b>""")

    text_prem_emoji = clean(f"""
        <b><emoji id="5116151848855667552">🚫</emoji> <u>{new_name}</u> вы поставили слишком большую ставку!

        <blockquote>• Максимальная ставка: {await db.admin.get_value('Max_Dep')} <emoji id='5409048419211682843'>💵</emoji>
        • Бот вернет вам: {koma} <emoji id='5409048419211682843'>💵</emoji></blockquote></b>""")

    return text, text_prem_emoji

async def check_reklama_user(name, stavka, value, user_id, bot: Bot, stavka_bot = False,):

    new_name = await clean_name(name, user_id)
    bonus_percent, value = await get_bonus(user_id, value, name)
    
    user = await db.users.get_user(user_id)
    level = await db.users.get_level_by_id(user['level_id'])
    text, text_prem_emoji = await build_text(new_name, stavka, value, level['name'], bonus_percent, stavka_bot)
    max_dep = float(await db.admin.get_value('Max_Dep'))

    if value > max_dep:

        # // СЧИТАЕМ НАШ ПРОФИТ С ЕГО ОШИБКИ (10%)
        koma_ = float(value) * 0.9
        koma = round(koma_, 2)
        update_profit = float(value) - float(koma)

        await db.users.add_balance(user_id, koma)
        await db.admin.plus_admin_profit(update_profit)

        text_error, text_prem_emoji_error = await build_max_dep_text(new_name, koma)
        try:
            soo = await cfg.pyro_client.send_message(
                chat_id=channel_game_id,
                caption=text_prem_emoji_error,
                disable_web_page_preview=True
            )
            try:
                await bot.edit_message_reply_markup(
                    chat_id=channel_game_id,
                    message_id=soo.id,
                    reply_markup=keyboard_error_user_id()
                )
            except Exception as inner_e:
                pass
            soo_id = soo.id

        except Exception as outer_e:
            soo = await bot.send_message(
                chat_id=channel_game_id,
                caption=text_error,
                disable_web_page_preview=True,
                reply_markup=keyboard_error_user_id()
            )
            soo_id = soo.message_id
        print('g')
        return soo_id, False, new_name, value

    try:
        soo = await cfg.pyro_client.send_message(
            chat_id=channel_game_id,
            caption=text_prem_emoji,
            disable_web_page_preview=True
        )
        try:
            await bot.edit_message_reply_markup(
                chat_id=channel_game_id,
                message_id=soo.id,
                reply_markup=keyboard_error_user_id()
            )
        except Exception as inner_e:
            pass
        soo_id = soo.id

    except Exception as outer_e:
        soo = await bot.send_message(
            chat_id=channel_game_id,
            caption=text,
            disable_web_page_preview=True,
            reply_markup=keyboard_error_user_id()
        )
        soo_id = soo.message_id

    return soo_id, True, new_name, value

async def handle_invalid_bet(stavka, value, soo, user_id, name, bot: Bot):
    if stavka not in invalid_stavki:

        koma_ = float(value) * 0.9
        koma = round(koma_, 2)
        await db.users.add_balance(user_id, koma)

        update_profit = float(value) - float(koma)
        await db.admin.plus_admin_profit(update_profit)

        try:
            await bot.delete_message(channel_game_id, soo)
        except:
            pass

        try:
            await asyncio.sleep(0.8)
            await cfg.pyro_client.send_message(chat_id=channel_game_id,
                                    caption=clean(f"""
                                    <b><emoji id='4927486932113425461'>❗</emoji> Бот заметил ошибку!</b>
                                               
                                    <blockquote><b><emoji id='5017088445353296841'>🔎</emoji> Вы забыли указать комментарий или указали его не верно! <emoji id='5445221832074483553'>💼</emoji> Бот вернет вам {koma} <emoji id='5409048419211682843'>💵</emoji> на ваш баланс</b></blockquote>"""))
        except Exception as e:
            await bot.send_message(chat_id=channel_game_id,
                                    caption=clean(f"""
                                    <b>❗ Бот заметил ошибку!</b>
                                               
                                    <blockquote><b>🔎 Вы забыли указать комментарий или указали его не верно! 💼Бот вернет вам {koma}$ на ваш баланс</b></blockquote>"""),
                                    reply_markup=keyboard_error_user_id())
        return False
    else:
        return True
    

async def check_referal_balance_turnover(user_id, amount, bot: Bot):
    ref_id = await db.referals.get_ref_id(user_id)
    referal_id = ref_id

    if referal_id != None:
        referal_percent_value = await db.admin.get_value('Referal_Precent')

        if isinstance(referal_percent_value, set):
            referal_percent_values = next(iter(referal_percent_value), 0)

            amount_ref_balance = float(amount) * (float(referal_percent_values) / 100)
            await db.referals.add_referal_balance(referal_id, amount_ref_balance)
            await db.referals.add_referal_turnover(ref_id, amount_ref_balance)
            try:
                if await db.referals.get_referal_notification(referal_id):
                    await bot.send_message(referal_id, f"<b>🐬 Ваш Реф.Баланс пополнен на <code>{round(amount_ref_balance, 2)}$</code></b>")
            except:
                pass

        else:

            amount_ref_balance = float(amount) * (float(referal_percent_value) / 100)
            await db.referals.add_referal_balance(referal_id, amount_ref_balance)
            await db.referals.add_referal_turnover(ref_id, amount_ref_balance)
            try:
               if await db.referals.get_referal_notification(referal_id):
                    await bot.send_message(referal_id, f"<b>🐬 Ваш Реф.Баланс пополнен на <code>{round(amount_ref_balance, 2)}$</code></b>")
            except:
                pass

    else:

        pass

async def check_user_level_up(user_id: int, bot: Bot):
    
    user = await db.users.get_user(user_id)
    if not user:
        return False

    current_turnover = user["turnover"]
    current_level_id = user["level_id"]
    current_level = await db.users.get_level_by_id(current_level_id)

    if not current_level:
        return False

    next_level = await db.users.get_level_by_id(current_level_id + 1)
    if not next_level:
        return False

    if current_turnover < next_level["required_turnover"]:
        return False

    await db.users.update_user_level(user_id, next_level["id"])

    reward = next_level["reward"]
    if reward > 0:
        await db.users.add_balance(user_id, reward)

    upcoming_level = await db.users.get_level_by_id(next_level["id"] + 1)
    if upcoming_level:
        needed = upcoming_level["required_turnover"] - current_turnover
        next_text = (
            f"➡ Следующая лига: {upcoming_level['name']} "
            f"({upcoming_level['required_turnover']}$)\n"
            f"Осталось набрать: <code>{needed:.2f}$</code>"
        )
    else:
        next_text = "🔥 Вы достигли максимальной лиги!"

    message_text = clean(f"""
        <blockquote><b>🆙 Новая лига!</b></blockquote>

        <b>🎉 Лига повышена до: {next_level['name']}
        🎁 Получена награда: <code>{reward}$</code></b>

        <b>{next_text}</b>""")

    try:
        await bot.send_message(
            chat_id=user_id,
            caption=message_text,
            parse_mode="HTML"
        )
    except Exception as e:
        pass

    return True

def normalize_stavka(stavka: str) -> str:
    return stavka.lower().replace('ё', 'е').strip()

def get_game_coefficient(stavka: str) -> float:
    stavka = normalize_stavka(stavka)

    for coef, variants in GAME_COEFFICIENTS.items():
        if stavka in variants:
            return coef

    return 99