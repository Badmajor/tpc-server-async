import asyncio
import logging
from datetime import datetime

from config import HOST, PORT
from database import AsyncDatabase


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def server_is_healthy(host, port) -> bool:
    """Метод проверяет готов ли сервер принимать подключения"""
    try:
        _, writer = await asyncio.open_connection(host=host, port=port)
        writer.close()
        return True
    except ConnectionRefusedError:
        return False


async def handle_client(reader, writer):
    """Обработчик входящих подключений"""
    addr = writer.get_extra_info("peername")
    logger.info(f"Connection from {addr}")
    while not reader.at_eof():
        data = await reader.read(50)
        if data:
            message = data.decode()
            timestamp = datetime.now().isoformat()
            async with AsyncDatabase() as db:
                await db.insert_message(str(addr), message, timestamp)

            writer.write(data)
            await writer.drain()

    logger.info(f"Connection with {addr} closed")
    writer.close()
    await writer.wait_closed()


async def start_server():
    """Запуск сервера"""
    server = await asyncio.start_server(handle_client, host=HOST, port=PORT)

    async with server:
        logger.info(f"Start server on {HOST}:{PORT}")
        await server.serve_forever()
