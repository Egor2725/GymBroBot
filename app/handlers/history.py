from aiogram import types, Router, F

router = Router()


@router.callback_query(F.data == 'history')
async def history(callback: types.CallbackQuery):
    await callback.answer('Раздел в разработке', show_alert=True)


