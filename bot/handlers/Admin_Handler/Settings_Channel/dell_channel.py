# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

# other
from data.config import db
from keyboards.Admin_Keyboards.Settings_Redact_Channel_Keyboard.settings_redact_channel_key import back_in_redact_channel_keyboard

router = Router()
class DellChannelState(StatesGroup):

    name_channel = State()

@router.callback_query(F.data == 'channel_admin_dell')
async def call_channel_admin_dell(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        return
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=f"<b>✍🏻 Введите название канала для удаления:</b>",
                                        reply_markup=back_in_redact_channel_keyboard())
    await state.set_state(DellChannelState.name_channel)

@router.message(StateFilter(DellChannelState.name_channel))
async def message_dell_channel(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id
    name_channel = message.text

    photo = FSInputFile('photo/admin.jpg')
    if not await db.channels.channel_exists(name_channel):
        await message.bot.send_message(chat_id=user_id,
                                    caption=f"<b>❌ Данный канал не найден в нашем списке</b>",
                                    reply_markup=back_in_redact_channel_keyboard())
    else:
        await db.channels.remove_channel_from_bd(name_channel)
        await message.bot.send_message(chat_id=user_id,
                                     caption=f"<b>✅ Данный канал удален!</b>",
                                     reply_markup=back_in_redact_channel_keyboard())
        await state.clear()    