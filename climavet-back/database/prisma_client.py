from prisma import Prisma
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

class DatabaseManager:
    def __init__(self) -> None:
        self._client = Prisma()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[Prisma, None]:
        """Asynchronous context manager to get a connected Prisma client."""
        await self._client.connect()
        try:
            yield self._client
        finally:
            await self._client.disconnect()

    async def connect(self) -> None:
        """Connect the Prisma client."""
        await self._client.connect()
    async def disconnect(self) -> None:
        """Disconnect the Prisma client."""
        await self._client.disconnect()

    async def health_check(self) -> bool:
        """Check if the database connection is healthy."""
        try:
            await self._client.connect()
            return True
        except Exception:
            return False
        finally:
            await self._client.disconnect()

# Singleton instance of DatabaseManager
database_manager = DatabaseManager()
