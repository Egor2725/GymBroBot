from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboards as kb
import data
import const

router = Router()


class TrainFSM(StatesGroup):
    train_type = State()  # cardio or strength
    part: None = State()        # hand | body | leg
    train = State()       # squats, or push ups etc.


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    # TODO send hello message for new income user!

    await state.clear()
    await message.answer(
        f"Hello, {message.from_user.full_name}!\nWelcome to GymBro Bot!",
        reply_markup=kb.main
    )


@router.message(Command('help'))
async def help_message(message: types.Message):
    # TODO: make help command great!
    await message.answer(
        f"Help message with all commands",
        reply_markup=kb.get_train_type()
    )


@router.message(Command('add_set'))
async def sets(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    train_id = state_data.get('train')
    if train_id is None:
        await message.answer("Сперва надо выбрать упражнение")
        return await start(message)
    train_instance = data.get_train_by_id(train_id)
    try:
        weight, times = message.text.replace('/add_set', '').split()
    except ValueError as err:
        print(err)  # TODO add to logs
        await message.answer(
            f"Упс, что-то пошло не так"
        )
        return

    await message.answer(
        f"Добавлен подход для {train_instance}\n{weight} kg X {times} повторов"
    )


@router.message(Command('set_done'))
async def train_done(message: types.Message, state: FSMContext):
    await message.reply('Отлично! тренировка завершена')
    await state.clear()
    return await start(message)


@router.callback_query(F.data.startswith('add_train'))
async def add_train(callback: types.CallbackQuery, state: FSMContext):
    state_name = await state.get_state()
    callback_date = callback.data.replace('add_train', '')
    msg, markup = "Ниченр не выбрано", None

    # TODO thinking, how to rewrite?
    if state_name is None:
        await state.set_state(TrainFSM.train_type)
        msg = 'Chose train type'
        markup = kb.get_train_type()

    elif state_name == TrainFSM.train_type:
        await state.update_data(train_type=callback_date)
        if callback_date == const.TRAIN_TYPE_CARDIO:
            await state.set_state(TrainFSM.train)
        else:
            await state.set_state(TrainFSM.part)

        msg = 'Chose part of body'
        markup = kb.get_parts()

    # TODO don't check part for cardio
    elif state_name == TrainFSM.part:
        await state.update_data(part=callback_date)
        state_data = await state.get_data()
        await state.set_state(TrainFSM.train)
        train_type = state_data['train_type']
        part = state_data.get('part')
        msg = 'Chose train'
        markup = kb.get_train(train_type=train_type, part=part)

    elif state_name == TrainFSM.train:
        await state.update_data(train=callback_date)
        await state.set_state(TrainFSM.train)
        msg = 'Add set /add_set {weight} {times}'

    await callback.message.edit_text(msg, reply_markup=markup)


@router.callback_query(F.data == 'history')
async def history(callback: types.CallbackQuery):
    await callback.answer('Раздел в разработке', show_alert=True)


@router.callback_query(F.data == 'recommends')
async def history(callback: types.CallbackQuery):
    await callback.answer('Раздел в разработке', show_alert=True)


@router.callback_query(F.data == 'report')
async def history(callback: types.CallbackQuery):
    await callback.answer('Раздел в разработке', show_alert=True)
