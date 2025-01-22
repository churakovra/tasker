import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import *

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_routers(
    add_router,
    delete_router,
    clear_router,
    list_router
)


async def main():
    bot = Bot(token=config.token)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
