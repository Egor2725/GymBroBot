from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.train import User,  Exercise
from app.const import TRAIN_TYPE_CARDIO

from .utils import extract_weight_and_times_from_message

router = Router()


class TrainFSM(StatesGroup):
    select_train_type = State()  # cardio or strength
    select_part = State()        # hand | body | leg
    select_train = State()       # squats, or push ups etc.
    complete = State()


class TrainMenuAdapter:
    def __init__(self, state: FSMContext, callback_data):
        self._state = state
        self._callback_data = callback_data

    def is_cardio(self):
        return self._callback_data == TRAIN_TYPE_CARDIO

    async def next(self):
        state = await self._state.get_state()
        if state is None:
            await self._state.set_state(TrainFSM.select_train_type)

        if state == TrainFSM.select_train_type:
            await self._state.update_data(train_type=self._callback_data)
            if not self.is_cardio():
                await self._state.set_state(TrainFSM.select_part)
            else:
                await self._state.set_state(TrainFSM.select_train)

        if state == TrainFSM.select_part:
            await self._state.update_data(part=self._callback_data)
            await self._state.set_state(TrainFSM.select_train)
        if state == TrainFSM.select_train:
            await self._state.update_data(train=self._callback_data)
            await self._state.set_state(TrainFSM.complete)

        return await self._state.get_state()

    async def prev(self):
        state = await self._state.get_state()
        if state == TrainFSM.select_train_type:
            await self._state.set_state(None)
        if state == TrainFSM.select_part:
            await self._state.set_state(TrainFSM.select_train_type)
        if state == TrainFSM.select_train:
            if not self.is_cardio():
                await self._state.set_state(TrainFSM.select_part)
            else:
                await self._state.set_state(TrainFSM.select_train_type)
        if state == TrainFSM.complete:
            await self._state.set_state(TrainFSM.select_train)

        return await self._state.get_state()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user, created = await User.get_or_create(
        id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )

    if created:
        msg = f"Hello, {user.name}!\nWelcome to GymBro Bot!",
    else:
        msg = f"Hi {user.name}!"
    await state.clear()
    await message.answer(msg, reply_markup=kb.main)


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

    weight, times = extract_weight_and_times_from_message(message.text)
    if weight is None or times is None:
        await message.answer("Упс, что-то пошло не так.")
        return

    exercise = await Exercise.get(int(train_id))
    await message.answer(
        f"Добавлен подход для {exercise.name}\n{weight} kg X {times} повторов"
    )


@router.message(Command('set_done'))
async def train_done(message: types.Message, state: FSMContext):
    await message.reply('Отлично! Упражнение завершено')
    await state.clear()


@router.callback_query(F.data.startswith('add_train'))
async def add_train(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.replace('add_train', '')
    is_back = callback_data == '_back'

    adapter = TrainMenuAdapter(state, callback_data=callback_data)
    if is_back:
        state_resolve = await adapter.prev()
    else:
        state_resolve = await adapter.next()

    match state_resolve:
        case TrainFSM.select_train_type.state:
            msg = 'Chose train type'
            markup = kb.get_train_type()
        case TrainFSM.select_part.state:
            msg = 'Chose part of body'
            markup = kb.get_parts()
        case TrainFSM.select_train.state:
            msg = 'Chose train'
            state_data = await state.get_data()
            train_type = state_data.get('train_type')
            part = state_data.get('part')
            exercises = await Exercise.filter_by_train_type_and_part(train_type, part)
            markup = kb.render_exercise(exercises)
        case TrainFSM.complete.state:
            msg = 'Add set /add_set {weight} {times}'
            markup = None
        case _:
            msg = 'On main menu.'
            markup = kb.main

    await callback.message.edit_text(msg, reply_markup=markup)



