class AdminDB:
    def __init__(self, db_core):
        self.db = db_core

    async def admin_exists(self, user_id: int) -> bool:
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT 1 FROM admin.admins WHERE user_id = $1",
                user_id
            )
            return bool(result)
        
    async def get_value(self, name: str):
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT value FROM admin.value WHERE name_value = $1",
                name
            )
            return float(result) if result else None
        
    async def update_value(self, name: str, value: float):
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval(
                "UPDATE admin.value SET value = $1 WHERE name_value = $2",
                value, name
            )
            return result
        
    async def reset_amount(self, name):
        async with self.db.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    "UPDATE admins.statistics SET value = 0 WHERE name_value = $1", name
                )
    
    async def get_statistic_value(self, name: str):
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT value FROM admin.statistics WHERE name_value = $1",
                name
            )
            return result
        
    async def get_all_statistics(self):
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT name_value, value FROM admin.statistics"
            )
        return {row['name_value']: row['value'] for row in rows}

    async def plus_admin_statistick(self, name: str, value: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE admin.statistics SET value = value + $1 WHERE name_value = $2",
                value, name
            )
    
    async def plus_admin_profit(self, value: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE admin.statistics
                SET value = value + $1
                WHERE name_value IN ('Profit', 'ProfitWeek', 'ProfitDay')
                """,
                value
            )

    async def minus_admin_profit(self, value: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE admin.statistics
                SET value = value - $1
                WHERE name_value IN ('Profit', 'ProfitWeek', 'ProfitDay')
                """,
                value
            )

    async def get_users(self):
        async with self.db.pool.acquire() as conn:
            query = "SELECT user_id FROM public.users"
            rows = await conn.fetch(query)
            return [row['user_id'] for row in rows]
        
    async def get_total_users(self):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM public.users"
            )
        
    async def get_total_turnover(self):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COALESCE(SUM(turnover), 0) FROM public.users_date"
            )

    async def get_win_lose_stats(self):
        async with self.db.pool.acquire() as conn:
            wins = await conn.fetchval(
                "SELECT COALESCE(SUM(win_game), 0) FROM public.users_date"
            )
            loses = await conn.fetchval(
                "SELECT COALESCE(SUM(lose_game), 0) FROM public.users_date"
            )
            return wins, loses

    async def get_statistick(self, name: str):
        async with self.db.pool.acquire() as conn:
            result = await conn.fetchval("SELECT value FROM admin.statistics WHERE name_value = $1", name)
            return float(result) if result else 0
