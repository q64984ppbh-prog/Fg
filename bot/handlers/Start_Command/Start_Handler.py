# main
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# other
from data.config import db, name_casino, url_project
from utils.help_function import clean
from utils.function_bot import check_registration
from utils.decorators import check_channels, require_subscription
from keyboards.Start_Keyboards.subscription_keyboard import markup_channels
from keyboards.Start_Keyboards.start_keyboard import start_keyboard_inline
from keyboards.Admin_Keyboards.Logs_Keyboard.logs_keyboard import referals_keyboard
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import start_withdraw_keyboard
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import (
    start_deposit_keyboard,
)


router = Router()

@router.message(Command('start'))
async def message_start_command(message: Message, state: FSMContext, command: CommandObject):

    await state.clear()
    args = command.args
    bot = message.bot

    user_id = message.from_user.id 
    first_name = message.from_user.first_name
    username = message.from_user.username
    message_id = message.message_id

    if message.chat.type != "private":
        await bot.send_message(
            chat_id=message.chat.id,
            caption=f"<b>🎰 Начни играть прямо сейчас в <a href='{url_project}'>{name_casino}</a></b>",
            disable_web_page_preview=True
        )
        return

    is_subscribed, unsubscribed_channels = await check_channels(user_id, bot)
    if not is_subscribed:
        photo = FSInputFile('photo/start.jpg')
        await bot.send_message(chat_id=user_id,
                             caption="<b>📌 Необходимо подписаться на все каналы!</b>",
                             reply_markup=markup_channels(unsubscribed_channels, args))
        return

    await check_registration(username, user_id, first_name, args, bot)
    async def check_admin(user_id):
        return "<i>👨‍💻 Админ панель активна</i>" if await db.admin.admin_exists(user_id) else ""

    if args and args == "dep":
        photo = FSInputFile('photo/profile.jpg')
        await bot.send_message(chat_id=user_id,
                             caption=clean(f"""
                                <b>📥 Пополнение</b> баланса
                                    
                                <blockquote>💭 <b>Большие победы</b> начинаются с маленьких пополнений.</blockquote>             
                                🦋 Выберите <b>платежную</b> систему:"""),
                                reply_markup=start_deposit_keyboard())
        return
    
    elif args and args == "withdraw":
        photo = FSInputFile('photo/profile.jpg')
        await bot.send_message(chat_id=user_id,
                            caption=clean(f"""
                                        <b>📤 Вывод</b> баланса
                                    
                                        <blockquote>💭 <b>Выиграл</b> — забери своё. Пусть твои победы звучат не цифрами на балансе, а звонкими монетами на счёте.</blockquote>             
                                        🦋 Выберите <b>платежную</b> систему:"""),
                            reply_markup=start_withdraw_keyboard())
        return
    
    elif args and args.startswith("checkreferaladmin_"):
        target_id = int(args.replace("checkreferaladmin_", ""))

        if not await db.admin.admin_exists(user_id):
            return

        referals = await db.referals.get_referals(target_id)
        if not referals:
            await bot.send_message(
                user_id,
                f"🙅‍♂️ У пользователя <code>{target_id}</code> нет рефералов."
            )
            return

        referals = list(referals)[::-1]
        page = 1
        per_page = 10

        try:
            await bot.send_message(
                chat_id=user_id,
                caption=(
                    f"<b>👥 Просматриваем рефералов пользователя <code>{target_id}</code></b>\n\n"
                    f"<b>🔎 Всего:</b> {len(referals)} чел.\n"
                    f"<b>🧾 Страница {page}</b>"
                ),
                reply_markup=referals_keyboard(
                    referals=referals,
                    page=page,
                    per_page=per_page,
                    owner_id=target_id,
                    safe=False
                ),
                disable_web_page_preview=True
            )

        except TelegramBadRequest as e:
            if "BUTTON_USER_PRIVACY_RESTRICTED" in str(e):
                await bot.send_message(
                    chat_id=user_id,
                    caption=(
                        f"<b>👥 Просматриваем рефералов пользователя <code>{target_id}</code></b>\n\n"
                        f"<b>🔎 Всего:</b> {len(referals)} чел.\n"
                        f"<b>🧾 Страница {page}</b>"
                    ),
                    reply_markup=referals_keyboard(
                        referals=referals,
                        page=page,
                        per_page=per_page,
                        owner_id=target_id,
                        safe=True
                    ),
                    disable_web_page_preview=True
                )
            else:
                raise

        return

    photo = FSInputFile('photo/start.jpg')
    await bot.send_message(chat_id=user_id,
                         text=clean(f"""
                        👋🏻 Добро пожаловать в <b><a href='{url_project}'>{name_casino}</a></b>

                        {await check_admin(user_id)}"""),
                        message_effect_id="5046509860389126442",
                        reply_markup=await start_keyboard_inline(user_id))
    
@router.callback_query(F.data == 'back_start')
async def call_back_start(call: CallbackQuery):

    bot = call.bot
    user_id = call.from_user.id 
    message_id = call.message.message_id

    async def check_admin(user_id):
        if not await db.admin.admin_exists(user_id):
            return ""
        else:
            return "<i>👨‍💻 Админ панель активна</i>"

    await call.answer()
    media = InputMediaPhoto(
        media=FSInputFile('photo/start.jpg'),
        caption=clean(f"""
                        👋🏻 Добро пожаловать в <b><a href='{url_project}'>{name_casino}</a></b>

                        {await check_admin(user_id)}""")
    )
    await bot.edit_message_media(chat_id=user_id,
                         message_id=message_id,
                        media=media,
                        reply_markup=await start_keyboard_inline(user_id))
    

@router.callback_query(F.data.startswith("ref_page"))
async def callback_ref_page(call: CallbackQuery):
    _, target_id, page = call.data.split(":")
    target_id = int(target_id)
    page = int(page)

    if not await db.admin.admin_exists(call.from_user.id):
        return

    referals = await db.referals.get_referals(target_id)
    if not referals:
        await call.message.edit_text("Нет рефералов.")
        return

    referals = list(referals)[::-1]
    per_page = 10

    await call.message.edit_text(
        caption=f"<b>👥 Просматриваем рефералов пользователя <code>{target_id}</code></b>\n\n"
             f"<b>🔎 Всего:</b> {len(referals)} чел.\n"
             f"<b>🧾 Страница {page}</b>",
        reply_markup=referals_keyboard(
            referals=referals,
            page=page,
            per_page=per_page,
            owner_id=target_id
        ),
        disable_web_page_preview=True
    )

    await call.answer()
