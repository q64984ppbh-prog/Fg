class GameChannelsDB:
    def __init__(self, db_core):
        self.db = db_core

    async def add_bet_to_queue(self, name: str, user_id: int, value: float, stavka: str, message_id: int, source: str = 'cryptobot'):
        async with self.db.pool.acquire() as conn:
            bet_id = await conn.fetchval(
                """
                INSERT INTO public.channelbet (name, user_id, value, stavka, message_id, status, source)
                VALUES ($1, $2, $3, $4, $5, 'pending', $6)
                RETURNING id
                """,
                name, user_id, value, stavka, message_id, source
            )
            return bet_id


    async def update_bet_status(self, bet_id: int, status: str):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.channelbet SET status = $1 WHERE id = $2",
                status, bet_id
            )

    
    async def update_channel_post_id(self, bet_id: int, channel_post_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "UPDATE public.channelbet SET channel_post_id = $1 WHERE id = $2",
                channel_post_id, bet_id
            )

    async def get_channel_post_id(self, bet_id: int):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT channel_post_id FROM public.channelbet WHERE id = $1",
                bet_id
            )

    async def dell_queue(self, bet_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM public.channelbet WHERE id = $1",
                bet_id
            )