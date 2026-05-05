from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import asyncpg


class DbClient:
    def __init__(self, dsn: str):
        self.db_conn_str = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.db_conn_str)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    # Handles connection pool management, gets a connection from the pool and releases it when done
    @asynccontextmanager
    async def get_db_conn(self) -> AsyncIterator[asyncpg.Connection]:
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            yield conn
