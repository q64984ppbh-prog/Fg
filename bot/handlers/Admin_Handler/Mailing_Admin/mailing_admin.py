# main
from aiogram import Router
from data.config import db

from aiogram import types, F
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# other
from keyboards.Admin_Keyboards.start_admin_keyboard import back_in_admin_keyboard

router = Router()
class MailingStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_caption = State()


@router.callback_query(F.data == "mailing_project")
async def start_send_message(call: types.CallbackQuery, state: FSMContext):

    user_id = call.from_user.id
    message_id = call.message.message_id

    await call.answer("👉🏻 Админ-Рассылка")
    await call.bot.edit_message_caption(
        chat_id=user_id,
        message_id=message_id,
        caption="<b>✍🏻 Отправьте изображение | текст для рассылки без изображений\n"
                "<code>(текст, фото, видео, GIF, документ):</code></b>",
        reply_markup=back_in_admin_keyboard()
    )

    await state.set_state(MailingStates.waiting_for_content)


@router.message(MailingStates.waiting_for_caption)
async def process_caption(message: types.Message, state: FSMContext):
    caption = None if message.text == "/skip" else message.text
    await send_mailing(message, caption, state)


@router.message(MailingStates.waiting_for_content)
async def process_mailing(message: types.Message, state: FSMContext):

    if message.text:
        await send_mailing(message, message.text, state)
        return

    media_type = None

    if message.photo:
        media_type = "photo"
        media = message.photo[-1].file_id
    elif message.video:
        media_type = "video"
        media = message.video.file_id
    elif message.animation:
        media_type = "animation"
        media = message.animation.file_id
    elif message.document:
        media_type = "document"
        media = message.document.file_id
    else:
        await message.answer("❌ Не поддерживаемый тип сообщения.")
        return

    await state.update_data(media=media, media_type=media_type)

    photo = FSInputFile("photo/admin.jpg")
    await message.bot.send_message(
            chat_id=message.from_user.id,
            caption="<b>⚠️ Введите подпись или отправьте /skip</b>",
            reply_markup=back_in_admin_keyboard()
    )

    await state.set_state(MailingStates.waiting_for_caption)


async def send_mailing(message: types.Message, caption: str, state: FSMContext):

    admin_id = message.from_user.id
    data = await state.get_data()
    media_type = data.get("media_type")
    media = data.get("media")

    users = await db.admin.get_users()
    success_count = 0

    await state.clear()
    await message.bot.send_message(chat_id=admin_id, text="<b>💭 Рассылка запущена. Ждите...</b>")

    for user_id in users:
        if user_id == admin_id:
            continue

        try:
            if media_type == "photo":
                await message.bot.send_message(user_id, media, text=caption)
            elif media_type == "video":
                await message.bot.send_video(user_id, media, text=caption)
            elif media_type == "animation":
                await message.bot.send_animation(user_id, media, text=caption)
            elif media_type == "document":
                await message.bot.send_document(user_id, media, text=caption)
            else:
                await message.bot.send_message(user_id, caption)

            success_count += 1

        except Exception as e:
            continue

    photo = FSInputFile("photo/admin.jpg")
    await message.bot.send_message(
            chat_id=admin_id,
            caption=f"<b>👉🏻 Рассылка завершена\n"
                    f"👤 <code>{success_count} человек</code> получили рассылку</b>",
            reply_markup=back_in_admin_keyboard()
    )
