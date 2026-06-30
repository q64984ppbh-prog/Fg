class SendDB:
    def __init__(self, db_core):
        self.db = db_core

    async def add_out_to_check(self, amount, user_id, username):
        async with self.db.pool.acquire() as connection:
            try:
                query = """
                    INSERT INTO public.out_queue (amount, user_id, username) 
                    VALUES ($1, $2, $3)
                """
                await connection.execute(query, amount, user_id, username)
            except Exception as e:
                pass

    async def update_check_status(self, bet_id, status):
        async with self.db.pool.acquire() as connection:
            query = 'UPDATE public.out_queue SET status = $1 WHERE id = $2'
            try:
                await connection.execute(query, status, bet_id)
            except Exception as e:
                pass

    async def dell_check(self, bet_id):
        async with self.db.pool.acquire() as connection:
            query = 'DELETE FROM public.out_queue WHERE id = $1'
            try:
                await connection.execute(query, bet_id)
            except Exception as e:
                pass