
import aiosqlite
import json

DB = "sleep.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS state (
            user_id INTEGER PRIMARY KEY,
            data TEXT
        )
        """)
        await db.commit()

async def load_state(user_id: int):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute(
            "SELECT data FROM state WHERE user_id=?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else None

async def save_state(user_id: int, state: dict):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "REPLACE INTO state (user_id, data) VALUES (?, ?)",
            (user_id, json.dumps(state))
        )
        await db.commit()