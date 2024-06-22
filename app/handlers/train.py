from aiogram import types, Router, F

from aiogram.fsm.context import FSMContext

from app import keyboards as kb
from app.database.train import Exercise, Train

from app.services.train_fsm import TrainFSMAdapter, resolve_message_and_markup, is_state_complete

from .utils import extract_weight_and_times_from_message

router = Router()


@router.message(F.text.startswith('Подход') | F.text.startswith('подход'))
async def add_set(message: types.Message, state: FSMContext):
    is_done = await is_state_complete(state)
    if not is_done:
        await message.answer("Сперва надо выбрать упражнение", reply_markup=kb.main)
        return

    weight, times = extract_weight_and_times_from_message(message.text)
    if weight is None or times is None:
        await message.answer("Упс, что-то пошло не так!\bМожет это были не цифры?, попробуй ещё раз.")
        return

    train_id = (await state.get_data())['train']
    exercise = await Exercise.get(int(train_id))

    await Train.create(
        exercise_id=exercise.id,
        user_id=message.from_user.id,
        weight=weight,
        times=times
    )
    await message.answer(
        f"Добавлен подход для *{exercise.name}*\n{weight} kg X {times} повторов"
    )


@router.message(F.text.startswith('Готово') | F.text.startswith('готово'))
async def add_set(message: types.Message, state: FSMContext):
    await message.reply('Отлично! Упражнение завершено')
    await state.clear()


@router.callback_query(F.data.startswith('add_train'))
async def add_train(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.replace('add_train', '')
    is_move_next = callback_data != '_back'
    adapter = TrainFSMAdapter(state, callback_data=callback_data)
    if is_move_next:
        current_state = await adapter.next()
    else:
        current_state = await adapter.prev()

    msg, markup = await resolve_message_and_markup(current_state, state)
    await callback.message.edit_text(msg, reply_markup=markup)



