# main
from aiogram import F, Router
from aiogram.types import FSInputFile, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Redact_Channel_Keyboard.settings_redact_channel_key import back_in_redact_channel_keyboard

router = Router()
class AddChannelState(StatesGroup):

    name_channel = State()
    chatid_channel = State()
    url_channel = State()

@router.callback_query(F.data == 'channel_amin_add')
async def call_channel_amin_add(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        return
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=f"<b>✍🏻 Введите название канала:</b>",
                                        reply_markup=back_in_redact_channel_keyboard())
    await state.set_state(AddChannelState.name_channel)

@router.message(StateFilter(AddChannelState.name_channel))
async def message_add_channel_name(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    photo = FSInputFile('photo/admin.jpg')

    name_channel = message.text
    await state.update_data(name_channel=name_channel)
    
    await message.bot.send_message(chat_id=user_id,
                                 text=f"<b>🆔 Введите ID канала:</b>",
                                 reply_markup=back_in_redact_channel_keyboard())
    await state.set_state(AddChannelState.chatid_channel)

@router.message(StateFilter(AddChannelState.chatid_channel))
async def message_add_channel_id(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    photo = FSInputFile('photo/admin.jpg')

    try:
        chatid_channel = int(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                     text=f"<b>❌ Введите верный ID канала!</b>",
                                     reply_markup=back_in_redact_channel_keyboard())
        return
    
    await state.update_data(chatid_channel=chatid_channel)
    await message.bot.send_message(chat_id=user_id,
                                 text=f"<b>💫 Введите URL ссылку канала!</b>",
                                 reply_markup=back_in_redact_channel_keyboard())

    await state.set_state(AddChannelState.url_channel)

@router.message(StateFilter(AddChannelState.url_channel))
async def message_add_channel_url(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    photo = FSInputFile('photo/admin.jpg')
    
    date = await state.get_data()
    url_channel = message.text
    chatid_channel = date.get('chatid_channel')
    name_channel = date.get('name_channel')

    await db.channels.add_channel(url_channel, chatid_channel, name_channel)
    await message.bot.send_message(chat_id=user_id,
                                 text=clean(f"""
                                <b>✅ Новый канал добавлен</b>
                                
                                <blockquote><b>✍️ Название:</b> <code>{name_channel}</code>
                                <b>🆔 Айди:</b> <code>{chatid_channel}</code>
                                <b>📎 Сслылка:</b> <code>{url_channel}</code></blockquote>"""),
                                reply_markup=back_in_redact_channel_keyboard())     
    await state.clear()