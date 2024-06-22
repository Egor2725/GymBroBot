import asyncio

from config import TOKEN

from aiogram import Bot, Dispatcher

from handlers import train_router, report_router, recommend_router, history_router


async def init():
    from app.database.data_migration import load_exercise
    print('start load_exercise')
    await load_exercise()
    print('complete load_exercise')


async def main():
    await init()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        train_router,
        history_router,
        recommend_router,
        report_router
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
