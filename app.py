import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.events import router
from storage.db import init_db

async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)

import asyncio
if __name__ == "__main__":
    asyncio.run(main())