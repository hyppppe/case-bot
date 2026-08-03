import aiosqlite

from config import START_BALANCE

DB_PATH = "database.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        await db.commit()


async def get_or_create_user(user_id: int, username: str | None) -> int:
    """Возвращает баланс пользователя, создавая запись при первом заходе."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row is not None:
            return row[0]

        await db.execute(
            "INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)",
            (user_id, username, START_BALANCE),
        )
        await db.commit()
        return START_BALANCE


async def get_balance(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else 0


async def change_balance(user_id: int, delta: int) -> int:
    """Атомарно изменяет баланс и возвращает новое значение."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (delta, user_id),
        )
        await db.commit()
        cursor = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0]
