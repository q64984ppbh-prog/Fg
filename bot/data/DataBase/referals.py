class ReferalDB:
    def __init__(self, db_core):
        self.db = db_core

    async def add_user_ref(self, user_id, referal_id=None):
        async with self.db.pool.acquire() as connection:
            async with connection.transaction():
                if referal_id is not None:
                    await connection.execute(
                        """
                        INSERT INTO public.referal_users (user_id, referal_id) 
                        VALUES ($1, $2)
                        """,
                        user_id, referal_id
                    )
                else:
                    await connection.execute(
                        """
                        INSERT INTO public.referal_users (user_id) 
                        VALUES ($1)
                        """,
                        user_id
                    )
            return True
        
    async def get_referals(self, user_id):
        async with self.db.pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT u.user_id, u.username, u.first_name, r.id
                FROM public.referal_users r
                LEFT JOIN public.users u ON u.user_id = r.user_id
                WHERE r.referal_id = $1
                ORDER BY r.id ASC
                """,
                user_id
            )
            return rows
        
    async def delete_user_referal(self, user_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE public.referal_users
                SET referal_id = NULL
                WHERE user_id = $1
                """,
                user_id
            )


    async def get_ref_id(self, user_id):
        async with self.db.pool.acquire() as connection:
            query = "SELECT referal_id FROM public.referal_users WHERE user_id = $1"
            result = await connection.fetchval(query, user_id)
            return result
        
    async def count_referals(self, user_id):
        async with self.db.pool.acquire() as connection:
            query = "SELECT COUNT(id) FROM public.referal_users WHERE referal_id = $1"
            result = await connection.fetchval(query, user_id)
            return result if result else 0
        
    async def get_referal_balance(self, user_id: int) -> float:
        async with self.db.pool.acquire() as conn:
            balance = await conn.fetchval(
                "SELECT ref_balance FROM public.referal_users WHERE user_id = $1",
                user_id
            )
            return float(balance) if balance is not None else 0.0
        
    async def get_referal_turnover(self, user_id: int) -> float:
        async with self.db.pool.acquire() as conn:
            balance = await conn.fetchval(
                "SELECT ref_turnover FROM public.referal_users WHERE user_id = $1",
                user_id
            )
            return float(balance) if balance is not None else 0.0
        
    async def add_referal_balance(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.referal_users SET ref_balance = ref_balance + $1 WHERE user_id = $2",
                amount, user_id
            )

    async def minus_referal_balance(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.referal_users SET ref_balance = ref_balance - $1 WHERE user_id = $2",
                amount, user_id
            )

    async def add_referal_turnover(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.referal_users SET ref_turnover = ref_turnover + $1 WHERE user_id = $2",
                amount, user_id
            )
    
    async def get_referal_notification(self, user_id):
        async with self.db.pool.acquire() as con:
            value = await con.fetchval(
                "SELECT ref_notifications FROM public.referal_users WHERE user_id = $1",
                user_id
            )
            return bool(value) if value is not None else False
        
    async def change_referal_notification(self, user_id, flag):
        async with self.db.pool.acquire() as con:
            await con.execute(
                "UPDATE public.referal_users SET ref_notifications = $1 WHERE user_id = $2",
                flag, user_id
            )

    async def get_referal_actual_bonus(self, user_id: int) -> float:
        async with self.db.pool.acquire() as conn:
            value = await conn.fetchval(
                "SELECT actual_bonus FROM public.referal_users WHERE user_id = $1",
                user_id
            )
            return value
        
    async def add_referal_bonus_turnover(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.referal_users SET bonus_turnover = bonus_turnover + $1 WHERE user_id = $2",
                amount, user_id
            )
        
    async def add_referal_actual_bonus(self, user_id: int, amount: float):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.referal_users SET actual_bonus = actual_bonus + $1 WHERE user_id = $2",
                amount, user_id
            )
        
    async def get_referal_turnover_bonus(self, user_id: int) -> float:
        async with self.db.pool.acquire() as conn:
            value = await conn.fetchval(
                "SELECT bonus_turnover FROM public.referal_users WHERE user_id = $1",
                user_id
            )
            return value