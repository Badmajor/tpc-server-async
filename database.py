import aiosqlite


class AsyncDatabase:
    def __init__(self, db_file="sqlite3.db"):
        self.db_file = db_file

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_file)
        await self._create_table()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await self.conn.commit()
            await self.conn.close()

    async def _create_table(self):
        await self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            addr TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
        )

    async def insert_message(self, addr, message, timestamp):
        await self.conn.execute(
            """
            INSERT INTO messages (addr, message, timestamp)
            VALUES (?, ?, ?)
            """,
            (addr, message, timestamp),
        )
