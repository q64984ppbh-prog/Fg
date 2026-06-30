import asyncpg
from asyncpg import Pool
from data.configure import (
    min_dep,
    max_dep,
    min_withdraw,
    min_ref_withdraw,
    flag_bonus_ref,
    amount_bonus_ref,
    flag_bonus_pripiska,
    referal_precent
)

class DatabaseCore:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pool: Pool | None = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.db_name,
            host=self.host,
            port=self.port,
            ssl=False
        )

        await self.ensure_default_values()
        await self.ensure_admin_default_values()

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def ensure_default_values(self):
        default_values = {
            "Min_Dep": min_dep,
            "Max_Dep": max_dep,
            "Min_Withdraw": min_withdraw,
            "Min_Ref_Withdraw": min_ref_withdraw,
            "Flag_Bonus_Ref": flag_bonus_ref,
            "Amount_Bonus_Ref": amount_bonus_ref,
            "Flag_Bonus_Pripiska": flag_bonus_pripiska,
            "Referal_Precent": referal_precent
        }

        async with self.pool.acquire() as conn:
            for name, value in default_values.items():
                row = await conn.fetchrow(
                    "SELECT 1 FROM admin.value WHERE name_value = $1",
                    name
                )
                if not row:
                    await conn.execute(
                        "INSERT INTO admin.value (name_value, value) VALUES ($1, $2)",
                        name, str(value)
                    )
                    

    async def ensure_admin_default_values(self):
        default_values = {
            "RefBonusCount": 0,
            "ProfitDay": 0,
            "ProfitWeek": 0,
            "Profit": 0,
            "Amount_Deposit": 0,
            "Amount_Replenishment": 0,
            "Amount_Replenishment_Day": 0,
        }

        async with self.pool.acquire() as conn:
            for name, value in default_values.items():
                row = await conn.fetchrow(
                    "SELECT 1 FROM admin.statistics WHERE name_value = $1",
                    name
                )
                if not row:
                    await conn.execute(
                        "INSERT INTO admin.statistics (name_value, value) VALUES ($1, $2)",
                        name, str(value)
                    )
                    