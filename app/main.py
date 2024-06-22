import asyncio

from config import TOKEN

from aiogram import Bot, Dispatcher

from handlers import router as base_router


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        base_router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
