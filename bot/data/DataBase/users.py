from decimal import Decimal
from datetime import datetime, timedelta, timezone

class UsersDB:
    def __init__(self, db_core):
        self.db = db_core

    async def user_exists(self, user_id: int) -> bool:
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT 1 FROM public.users WHERE user_id = $1",
                user_id
            )
            return bool(result)

    async def add_user(self, user_id, first_name, username):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO public.users (user_id, first_name, username) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO NOTHING",
                            user_id, first_name, username)

    async def add_user_game_data(self, user_id):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO public.users (user_id) VALUES ($1) ON CONFLICT (user_id) DO NOTHING", user_id)

    async def get_user(self, user_id: int):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM public.users_date WHERE user_id = $1",
                user_id
            )
        
    async def add_turnover(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET turnover = turnover + $1 WHERE user_id = $2",
                amount, user_id
            )

    async def add_win_game(self, user_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET win_game = win_game + 1 WHERE user_id = $1",
                user_id
            )

    async def update_user_level(self, user_id: int, new_level_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET level_id = $1 WHERE user_id = $2",
                new_level_id, user_id
            )

    async def add_lose_game(self, user_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET lose_game = lose_game + 1 WHERE user_id = $1",
                user_id
            )

    async def add_balance(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET balance = balance + $1 WHERE user_id = $2",
                amount, user_id
            )

    async def minus_balance(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET balance = balance - $1 WHERE user_id = $2",
                amount, user_id
            )

    async def try_reserve_balance(self, user_id: int, amount: Decimal) -> bool:
        async with self.db.pool.acquire() as con:
            result = await con.execute(
                """
                UPDATE public.users_date
                SET balance = balance - $1
                WHERE user_id = $2
                AND balance >= $1
                """,
                amount, user_id
            )

        return result == "UPDATE 1"


    async def add_replenishment(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET amount_replenishment = amount_replenishment + $1 WHERE user_id = $2",
                amount, user_id
            )

    async def add_withdraw(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.users_date SET amount_withdraw = amount_withdraw + $1 WHERE user_id = $2",
                amount, user_id
            )

    async def get_balance(self, user_id: int) -> float:
        async with self.db.pool.acquire() as conn:
            balance = await conn.fetchval(
                "SELECT balance FROM public.users_date WHERE user_id = $1",
                user_id
            )
            return float(balance) if balance is not None else 0.0
        
    async def update_max_win(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as con:
            await con.execute(
                """
                UPDATE users_date
                SET max_win = GREATEST(max_win, $1)
                WHERE user_id = $2
                """,
                amount,
                user_id
            )


    async def get_anonimnost(self, user_id: int):
        async with self.db.pool.acquire() as con:
            row = await con.fetchval("""
                SELECT anonimnost
                FROM public.users
                WHERE user_id = $1""", 
            user_id)
            return row

    async def update_anonimnost(self, user_id: int, anonimnost: bool):
        async with self.db.pool.acquire() as con:
            await con.execute(
                "UPDATE public.users SET anonimnost = $1 WHERE user_id = $2",
                anonimnost, user_id
            )

    async def add_user_stats(self, user_id, first_name):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO public.users_date (user_id, first_name) VALUES ($1, $2)",
                            user_id, first_name)
            
    async def get_levels(self):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM public.levels ORDER BY required_turnover ASC")
            return [dict(r) for r in rows]
        
    async def get_user_level(self, turnover: float):
        async with self.db.pool.acquire() as conn:
            level = await conn.fetchrow(
                """
                SELECT * FROM public.levels
                WHERE required_turnover <= $1
                ORDER BY required_turnover DESC
                LIMIT 1
                """,
                turnover
            )
            return dict(level) if level else None

    async def get_next_level(self, turnover: float):
        async with self.db.pool.acquire() as conn:
            next_level = await conn.fetchrow(
                """
                SELECT * FROM public.levels
                WHERE required_turnover > $1
                ORDER BY required_turnover ASC
                LIMIT 1
                """,
                turnover
            )
            return dict(next_level) if next_level else None
        
    async def get_level_by_id(self, level_id: int):
        async with self.db.pool.acquire() as conn:
            level = await conn.fetchrow(
                "SELECT * FROM public.levels WHERE id = $1",
                level_id
            )
            return dict(level) if level else None  

    async def add_history_replenishment(self, user_id, amount, system, date):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO history.history_deposit (user_id, amount, system, date) VALUES ($1, $2, $3, $4)",
                            user_id, amount, system, date)
            
    async def get_user_deposits(self, user_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT id, amount, system, date
                FROM history.history_deposit
                WHERE user_id = $1
            """, user_id)
            return rows
        
    async def get_user_deposits_by_id(self, deposit_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT user_id, amount, system, date
                FROM history.history_deposit
                WHERE id = $1
            """, deposit_id)
            return rows
        
    async def get_user_withdraw(self, user_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT id, amount, system, date
                FROM history.history_withdraw
                WHERE user_id = $1
            """, user_id)
            return rows
        
    async def get_user_withdraw_by_id(self, withdraw_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT user_id, amount, system, date
                FROM history.history_withdraw
                WHERE id = $1
            """, withdraw_id)
            return rows
        
    async def add_history_withdraw(self, user_id, amount, system, date):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO history.history_withdraw (user_id, amount, system, date) VALUES ($1, $2, $3, $4)",
                            user_id, amount, system, date)
            
    async def get_user_withdraw(self, user_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT id, amount, system, date
                FROM history.history_withdraw
                WHERE user_id = $1
            """, user_id)
            return rows
        
    async def get_user_withdraw_by_id(self, deposit_id: int):
        async with self.db.pool.acquire() as con:
            rows = await con.fetch("""
                SELECT user_id, amount, system, date
                FROM history.history_withdraw
                WHERE id = $1
            """, deposit_id)
            return rows
        
    async def get_info_date_by_id(self, user_id: int):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT *
                FROM public.users_date
                WHERE user_id = $1
            """, user_id)
            return rows
        
    
    async def check_user_throttle(self, user_id: int, action: str, rate: float):
        async with self.db.pool.acquire() as con:
            now = datetime.now(timezone.utc)
            row = await con.fetchrow(
                "SELECT last_call, exceeded_count FROM user_throttle WHERE user_id=$1 AND action=$2",
                user_id, action
            )

            if not row:
                await con.execute(
                    "INSERT INTO user_throttle(user_id, action, last_call, exceeded_count) VALUES ($1, $2, $3, 0)",
                    user_id, action, now
                )
                return "allowed"

            last_call = row["last_call"]
            exceeded_count = row["exceeded_count"]
            delta = (now - last_call).total_seconds()

            if delta < rate:
                new_count = exceeded_count + 1
                await con.execute(
                    "UPDATE user_throttle SET exceeded_count=$1, last_call=$2 WHERE user_id=$3 AND action=$4",
                    new_count, now, user_id, action
                )
                if new_count == 1:
                    return "notify_flood"
                return "silent_block"
            
            else:
                was_throttled = exceeded_count > 0
                
                await con.execute(
                    "UPDATE user_throttle SET last_call=$1, exceeded_count=0 WHERE user_id=$2 AND action=$3",
                    now, user_id, action
                )
                
                return "unblocked" if was_throttled else "allowed"


    async def update_last_notify(self, user_id: int, action: str, now: datetime):
        async with self.db.pool.acquire() as con:
            await con.execute(
                "UPDATE user_throttle SET last_notify=$1 WHERE user_id=$2 AND action=$3",
                now, user_id, action
            )