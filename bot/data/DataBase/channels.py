class ChannelsDB:
    def __init__(self, db_core):
        self.db = db_core

    async def get_channels(self):
        async with self.db.pool.acquire() as conn:
            result = await conn.fetch(
                "SELECT url_channel, chatid_channel, name_channel FROM admin.channels"
            )
            return result if result else []

    async def add_channel(self, url: str, chat_id: int, name: str):
        async with self.db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO admin.channels (url_channel, chatid_channel, name_channel)
                VALUES ($1, $2, $3)
            """, url, chat_id, name)

    async def remove_channel(self, chat_id: int):
        async with self.db.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM admin.channels WHERE chatid_channel = $1",
                chat_id
            )

    async def remove_channel_from_bd(self, name_channel):
        async with self.db.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    "DELETE FROM admin.channels WHERE name_channel = $1",
                    name_channel
                )
        return True

    async def get_all_channels(self):
        async with self.db.pool.acquire() as connection:
            results = await connection.fetch(
                """
                SELECT name_channel, chatid_channel, url_channel
                FROM admin.channels
                """
            )
            return results
        
    async def channel_exists(self, name_channel):
        async with self.db.pool.acquire() as connection:
            result = await connection.fetchval(
                "SELECT 1 FROM admin.channels WHERE name_channel = $1",
                name_channel
            )
            return result is not None