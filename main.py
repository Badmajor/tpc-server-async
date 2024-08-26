import asyncio
import logging

from client import client
from config import HOST, PORT, AMOUNT_CLIENTS
from server import server_is_healthy, start_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Start program")
    server_task = asyncio.create_task(start_server())

    while not await server_is_healthy(HOST, PORT):
        logger.info("Server is not ready for connections")
        await asyncio.sleep(1)

    client_tasks = [client() for _ in range(AMOUNT_CLIENTS)]

    await asyncio.gather(*client_tasks)

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        logger.info("Stop server")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program stopped by user")
