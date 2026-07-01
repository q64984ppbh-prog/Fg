# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_User_Profile_Keyboard.settings_user_profile_key import find_user_keyboard
from keyboards.Admin_Keyboards.start_admin_keyboard import (
    back_in_admin_keyboard
)

router = Router()
class FindUserAdminState(StatesGroup):

    us_id = State()

@router.callback_query(F.data == 'redact_user_statistics')
async def call_redact_user_statistics(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    await call.answer()
    await call.message.delete(); await call.bot.send_message(chat_id=user_id,
                                        
                                        text=clean(f"""
                                        <b>👤 Поиск пользователя</b>

                                        <blockquote>🔄 Вы сможете редактировать профиль пользователя и смотреть его!</blockquote>

                                        <b>✍🏻 Введите ID игрока:</b>"""),
                                        reply_markup=back_in_admin_keyboard())
    await state.set_state(FindUserAdminState.us_id)

@router.message(StateFilter(FindUserAdminState.us_id))
async def message_find_user_admin(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    
    try:
        pool_id = int(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                     text=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>

                                    <blockquote>❌ Вы ввели не верное число для <b>редактирования пользователя</b></blockquote>
                                     
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_admin_keyboard())
        return
    
    if not await db.users.user_exists(pool_id):
        await message.bot.send_message(chat_id=user_id,
                                     text=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>

                                    <blockquote>❌ Данный пользователь не найден в базе данных</blockquote>
                                     
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_admin_keyboard())
    
    else:
        info = await db.users.get_info_date_by_id(pool_id)

        for inf in info:

            level = await db.users.get_level_by_id(inf['level_id'])
            level_name = level['name'] if level else '❓ Неизвестно'

            await message.bot.send_message(chat_id=user_id,
                                        text=clean(f"""
                                        <b>👤 Найден пользователь: {inf['first_name']}</b>

                                        <blockquote><b>📊 Найденная информация:</b>
                                        
                                        🛡 Лига — <b>{level_name}</b>
                                        💰 Баланс — <b>{inf['balance']}$</b>
                                        💸 Оборот — <b>{inf['turnover']:.2f}$</b>
                                        🎲 Сыграно — <b>{inf['win_game'] + inf['lose_game']} шт.</b>
                                        📥 Пополнений — <b>{inf['amount_replenishment']}$</b>
                                        📤 Выводов — <b>{inf['amount_withdraw']}$</b>
                                        💸 Макс. вин — <b>{inf['max_win']}$</b></blockquote>
                                        
                                        <b>ℹ️ Выберите действия редактирования профиля:</b>"""),
                                        reply_markup=find_user_keyboard(pool_id))
        await state.clear()

@router.callback_query(F.data.startswith('back_in_find_'))
async def call_back_in_find(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    data = call.data.split('_')
    pool_id = int(data[3])

    await call.answer()
    info = await db.users.get_info_date_by_id(pool_id)
    for inf in info:

        level = await db.users.get_level_by_id(inf['level_id'])
        level_name = level['name'] if level else '❓ Неизвестно'

        await call.message.delete(); await call.bot.send_message(chat_id=user_id,
                                            
                                            text=clean(f"""
                                        <b>👤 Найден пользователь: {inf['first_name']}</b>

                                        <blockquote><b>📊 Найденная информация:</b>
                                        
                                        🛡 Лига — <b>{level_name}</b>
                                        💰 Баланс — <b>{inf['balance']}$</b>
                                        💸 Оборот — <b>{inf['turnover']:.2f}$</b>
                                        🎲 Сыграно — <b>{inf['win_game'] + inf['lose_game']} шт.</b>
                                        📥 Пополнений — <b>{inf['amount_replenishment']}$</b>
                                        📤 Выводов — <b>{inf['amount_withdraw']}$</b>
                                        💸 Макс. вин — <b>{inf['max_win']}$</b></blockquote>
                                        
                                        <b>ℹ️ Выберите действия редактирования профиля:</b>"""),
                                        reply_markup=find_user_keyboard(pool_id))