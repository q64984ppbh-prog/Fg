# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# other
from data.config import db, name_casino, username_bot_casino
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_User_Profile_Keyboard.settings_user_profile_key import find_user_keyboard
from keyboards.Admin_Keyboards.Settings_User_Profile_Keyboard.settings_user_profile_key import (
    back_in_find_user,
    succes_plus_balance_keyboard,
    succes_minus_balance_keyboard
)

router = Router()
class ChangeBalanceFindUser(StatesGroup):
    amount = State()

@router.callback_query(F.data.startswith('redact_admin_user_balance_'))
async def call_redact_admin_user_balance(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    data = call.data.split('_')
    pool_id = data[4]
    cho = data[5]

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🔄 Изменение баланса игрока</b>
                                                      
                                        <blockquote>ℹ️ Здесь вы можете изменить баланс игрока!</blockquote>
                                        
                                        ✍🏻 Введите сумму для <b>{"пополнения" if cho == 'plus' else "снижения"}</b> баланса пользователя:"""),
                                        reply_markup=back_in_find_user(pool_id))
    await state.set_state(ChangeBalanceFindUser.amount)
    await state.update_data(cho=cho, us_id=pool_id)

@router.message(StateFilter(ChangeBalanceFindUser.amount))
async def message_change_balance_admin(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id

    data = await state.get_data()
    cho = data.get('cho')
    pool_id = data.get('us_id')

    try:
        amount = float(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                    caption=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>

                                    <blockquote>❌ Вы ввели не верную сумму для <b>{"пополнения" if cho == 'plus' else "снижения"}</b></blockquote>
                                        
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_find_user(pool_id))
        return
    
    if cho == 'plus':
        await db.users.add_balance(int(pool_id), amount)

        try:
            await message.bot.send_message(chat_id=int(pool_id),
                                           caption=clean(f"""
                                            <b>🎁 Поздравляем! Ваш баланс был пополнен администрацией!</b>
                                                      
                                            <blockquote>🔄 Мы пополнили ваш баланс на сумму <b>{amount}$</b></blockquote>"""),
                                            reply_markup=succes_plus_balance_keyboard(username_bot_casino))
        except:
            pass

    elif cho == 'minus':
        await db.users.minus_balance(int(pool_id), amount)

        try:
            await message.bot.send_message(chat_id=int(pool_id),
                                           caption=clean(f"""
                                            <b>🧐 Что то случилось! Мы сняли ваш баланс!</b>
                                                      
                                            <blockquote>🔄 Мы сняли с вашего баланс <b>{amount}$</b></blockquote>"""),
                                            reply_markup=succes_minus_balance_keyboard(username_bot_casino))
        except:
            pass

    info = await db.users.get_info_date_by_id(int(pool_id))
    for inf in info:

        level = await db.users.get_level_by_id(inf['level_id'])
        level_name = level['name'] if level else '❓ Неизвестно'

        await message.bot.send_message(chat_id=user_id,
                                        caption=clean(f"""
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