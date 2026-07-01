# main
from data.config import db
from utils.help_function import decode_referral

async def process_referral(bot, user_id: int, first_name: str, args: str | None):
    referal_id = None

    if args and args.startswith("invite_"):
        ref_code = args.split("invite_")[1]

        if ref_code.isalnum() and len(ref_code) >= 6:
            try:
                decoded_id = decode_referral(ref_code)
                if decoded_id != user_id and await db.users.user_exists(decoded_id):
                    referal_id = decoded_id
            except Exception:
                pass

    await db.referals.add_user_ref(user_id, referal_id)
    if referal_id:
        try:
            await bot.send_message(
                chat_id=referal_id,
                text=f"<b>🎰 Ваш друг <code>{first_name}</code> присоединился по реферальной ссылке!</b>"
            )
        except Exception:
            pass

async def check_registration(username, user_id, first_name, command, bot):
    if not await db.users.user_exists(user_id):
        await db.users.add_user(user_id, first_name, username)
        await db.users.add_user_stats(user_id, first_name)
        await db.users.add_user_game_data(user_id)
        await process_referral(bot, user_id, first_name, command)

def normal_chance(N, M):
    if N <= 0 or M <= 0:
        return 0
    
    base = M / (25 - N)
    accelerator = 1 + ((N - 1) / 5) * (M / 10)
    chance = base * accelerator
    
    if N <= 10:
        chance = min(chance, 0.95)
    else:
        chance = min(chance, 0.99)
    
    return round(chance * 100, 1)