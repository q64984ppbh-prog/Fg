from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import start_deposit_keyboard
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import start_withdraw_keyboard
from keyboards.Start_Keyboards.start_keyboard import start_keyboard_inline
from keyboards.User_Keyboards.nav_keyboard import main_nav_keyboard
from utils.function_bot import check_registration

router = Router()

@router.message(Command('start'))
async def message_start_command(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()
    bot = message.bot
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    args = command.args

    await check_registration(username, user_id, first_name, args, bot)

    if args == "dep":
        await bot.send_message(chat_id=user_id, text=clean("""<b>📥 Пополнение</b> баланса

<blockquote>💭 <b>Большие победы</b> начинаются с маленьких пополнений.</blockquote>             
🦋 Выберите <b>платежную</b> систему:"""), reply_markup=start_deposit_keyboard())
        return

    if args == "withdraw":
        await bot.send_message(chat_id=user_id, text=clean("""<b>📤 Вывод</b> баланса

<blockquote>💭 <b>Выиграл</b> — забери своё.</blockquote>             
🦋 Выберите <b>платежную</b> систему:"""), reply_markup=start_withdraw_keyboard())
        return

    admin_text = "<i>👨‍💻 Админ панель активна</i>" if await db.admin.admin_exists(user_id) else ""
    await bot.send_message(
        chat_id=user_id,
        text=f"<tg-emoji emoji-id=\"4918354603281482671\">👋</tg-emoji> Добро пожаловать в @duckwin\n\n{admin_text}",
        parse_mode='HTML',
        reply_markup=await start_keyboard_inline(user_id)
    )
    

@router.callback_query(F.data == 'back_start')
async def call_back_start(call: CallbackQuery):
    user_id = call.from_user.id
    admin_text = "<i>👨‍💻 Админ панель активна</i>" if await db.admin.admin_exists(user_id) else ""
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        user_id,
        f"<tg-emoji emoji-id=\"4918354603281482671\">👋</tg-emoji> Добро пожаловать в @duckwin\n\n{admin_text}",
        parse_mode='HTML',
        reply_markup=await start_keyboard_inline(user_id)
    )
