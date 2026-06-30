from decimal import Decimal
import random
import json

class GameUserDB:
    def __init__(self, db_core):
        self.db = db_core

    async def count_mines(self, user_id):
        async with self.db.pool.acquire() as con:
            result = await con.fetchval("SELECT amount_mins FROM public.users_game_data WHERE user_id = $1", user_id)
            return result if result else 3
        
    async def update_count_mines(self, user_id, count):
        async with self.db.pool.acquire() as con:
            await con.execute(
                "INSERT INTO public.users_game_data (user_id, amount_mins) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET amount_mins = $2",
                user_id, count
            )
        
    async def create_mines_game(self, user_id: int, amount: Decimal, count_mines: int):
        total_cells = 25
        mines_positions = random.sample(range(total_cells), int(count_mines))

        async with self.db.pool.acquire() as con:
            query = """
            INSERT INTO mines_game (user_id, amount, mines_count, opened_cells, mines_position)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
            """
            game_id = await con.fetchval(
                query,
                user_id,
                amount,
                count_mines,
                '{}',
                json.dumps(mines_positions)
            )
            return game_id
        
    async def get_game(self, game_id: int):
        async with self.db.pool.acquire() as con:
            row = await con.fetchrow(
            """
            SELECT opened_cells, mines_position, mines_count, amount, status
            FROM mines_game
            WHERE id = $1
            """,
            game_id
            )
            if row:
                row = dict(row)
                if row.get('mines_position') and isinstance(row['mines_position'], str):
                    row['mines_position'] = json.loads(row['mines_position'])
                if row.get('opened_cells') and isinstance(row['opened_cells'], str):
                    row['opened_cells'] = json.loads(row['opened_cells'])
                return row
            return None

    async def open_cell(self, game_id: int, opened_cells: list):
        async with self.db.pool.acquire() as con:
            await con.execute(
            "UPDATE mines_game SET opened_cells=$1 WHERE id=$2",
            json.dumps(opened_cells),
            game_id
            )

    async def finish_game(self, game_id: int):
        async with self.db.pool.acquire() as con:
            await con.execute(
            "UPDATE mines_game SET status = 'finish' WHERE id=$1",
            game_id
            )

    async def update_mines(self, game_id: int, mines: list):
        async with self.db.pool.acquire() as con:
            await con.execute(
            """
            UPDATE mines_game
            SET mines_position = $1
            WHERE id = $2
            """,
            json.dumps(mines),
            game_id
            )
