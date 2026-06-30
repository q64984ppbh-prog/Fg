# main
from aiogram import Bot, Dispatcher, F
from config_reader import config
from data.config import db, api_id, api_hash, phone_number
from aiogram.client.default import DefaultBotProperties
import handlers
from aiogram.types import User
import data.config as cfg

# middleware
from Middleware.IgoneMessage import IgnoreMessageNotModifiedMiddleware
from Middleware.AntispamMiddleware import AntiFloodMiddleware

# Tire
from tire import start_scheduler

# other
import asyncio
from utils.channel_function.bet_function import process_bets_in_strict_sequence
from handlers.User_Command.Profile_Handler.Withdraw_Handler.CryptoBot.function_withdraw_cryptobot import process_outs_in_sequence

async def main():
    await db.core.connect()
    start_scheduler()

    bot = Bot(
            config.bot_token.get_secret_value(),
            default=DefaultBotProperties(parse_mode="HTML")
        )
    dp = Dispatcher()
    
    
    
    dp.message.middleware(IgnoreMessageNotModifiedMiddleware())
    dp.callback_query.middleware(IgnoreMessageNotModifiedMiddleware())
    dp.message.middleware(AntiFloodMiddleware())

    asyncio.create_task(process_bets_in_strict_sequence(db.core, bot))

    dp.include_routers(
        handlers.Start_Handler.router,
        handlers.check_sab.router,
        handlers.start_profile_handler.router,
        handlers.start_deposit_handler.router,
        handlers.deposit_cryptobot.router,
        handlers.start_statistick.router,
        handlers.start_tranzaction.router,
        handlers.start_withdraw.router,
        handlers.start_deposit_history.router,
        handlers.info_handler.router,
        handlers.start_history_withdraw.router,
        handlers.withdraw_cryptobot.router,
        handlers.start_referal_handler.router,
        handlers.deposit_chat.router,
        handlers.send_ref_money.router,
        handlers.change_notification_ref.router,
        handlers.start_referal_bonus.router,
        handlers.out_referal_bonus.router,
        handlers.league_bonus.router,
        handlers.check_out_ref.router,
        handlers.start_admin.router,
        handlers.start_bonus_handler.router,
        handlers.anonimnost_handler.router,
        handlers.start_create_game.router,
        handlers.start_settings_value.router,
        handlers.settings_max_or_min_deposit.router,
        handlers.settings_min_withdraw.router,
        handlers.deposit_xrocket.router,
        handlers.settings_ref_withdraw.router,
        handlers.start_settings_referal_bonus.router,
        handlers.change_amount_ref_bonus.router,
        handlers.start_find_user.router,
        handlers.redact_balance_user.router,
        handlers.start_nickname_bonus.router,
        handlers.nickaname_bonus.router,
        handlers.main_handler.router,
        handlers.change_referal_precent.router,
        handlers.start_settings_channel.router,
        handlers.add_channel.router,
        handlers.dell_referal_user.router,
        handlers.dell_channel.router,
        handlers.mailing_admin.router,
        handlers.start_statistick_admin.router,
        handlers.create_game.router,
        handlers.start_mines_game.router,
        handlers.change_count_mines.router,
        handlers.mines_game.router,
        #handlers.change_count_mines.router,
        #handlers.mines_game.router
    )

    bot_info: User = await bot.get_me()
    print(f"[🤖] Бот запущен: @{bot_info.username}")

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
            await db.core.close()

if __name__ == '__main__':
    asyncio.run(main())