# main
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Redact_Channel_Keyboard.settings_redact_channel_key import start_redact_channel_keyboard

router = Router()

@router.callback_query(F.data == 'channel_redact_project')
async def call_channel_redact_project(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    if not await db.admin.admin_exists(user_id):
        return
    
    channels = await db.channels.get_all_channels()

    if channels:
        channels_text = "\n".join(
            [
                f"🔹 <b>{chan['name_channel']}</b> (url: <code>{chan['url_channel']}</code>)"
                for chan in channels
            ]
        )
    else:
        channels_text = "<code>❌ Нет активных каналов.</code>"

    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>📕 Каналы подписки</b>
                                                      
                                        <blockquote><b>📊 Активные каналы</b>
                                                      
                                        {channels_text}</blockquote>

                                        <b>ℹ️ Что будем делать?</b>"""),
                                        reply_markup=start_redact_channel_keyboard())