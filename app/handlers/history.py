from aiogram import types, Router, F

from app.database.train import Train

router = Router()


@router.callback_query(F.data == 'history')
async def history(callback: types.CallbackQuery):
    trains = await Train.get_all_by_user_id(id=callback.from_user.id)
    train_str = ''.join([str(train) + '\n' for train in trains])
    msg = f'Тренировки:\n {train_str}'
    await callback.answer("процессим", cache_time=0)
    await callback.message.answer(msg)


