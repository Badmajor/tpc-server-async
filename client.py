import asyncio
import logging
from random import randrange

from config import HOST, PORT, AMOUNT_MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def client():
    """Метод создает подключение и отправляет
    5 сообщений с разным интервалом"""
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    addr = writer.get_extra_info("sockname")

    for i in range(AMOUNT_MESSAGES):
        await asyncio.sleep(randrange(5, 11))
        message = f"message_{i + 1} from client {addr}"
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(50)
        answer = data.decode()
        logger.info(f"Answer: {answer}")

    writer.close()
    await writer.wait_closed()
