# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

# other
from data.config import db, name_casino, url_project
from utils.help_function import decode_referral,  clean
from utils.decorators import check_channels
from utils.function_bot import check_registration
from keyboards.Start_Keyboards.start_keyboard import start_keyboard_inline
from keyboards.Start_Keyboards.subscription_keyboard import markup_channels

router = Router()

@router.callback_query(F.data.startswith('check_subscription'))
async def call_check_subscription_channels(call: CallbackQuery):

    user_id = call.from_user.id 
    first_name = call.from_user.first_name
    username = call.from_user.username
    message_id = call.message.message_id
    
    bot = call.bot
    dates = call.data.split(':')
    ref_args = dates[1]

    is_subscribed, unsubscribed_channels = await check_channels(user_id, bot)
    if not is_subscribed:
        await call.answer("❌ Проверка не пройдена", show_alert=True)
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text='<b>👉🏻 Подпишитесь на все каналы!</b>',
                reply_markup=markup_channels(unsubscribed_channels, ref_args))
        except:
            pass
        return

    else:
        await check_registration(username, user_id, first_name, ref_args, bot)
        async def check_admin(user_id):
            return "<i>👨‍💻 Админ панель активна</i>" if await db.admin.admin_exists(user_id) else ""
            
        await bot.edit_message_text(chat_id=user_id,
                        message_id=message_id,
                        text=clean(f"""
                        👋🏻 Добро пожаловать в <b><a href='{url_project}'>{name_casino}</a></b>

                        {await check_admin(user_id)}"""),
                        reply_markup=await start_keyboard_inline(user_id))