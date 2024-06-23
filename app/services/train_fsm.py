from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from const import TRAIN_TYPE_CARDIO
from database.train import Exercise
import keyboards as kb


class TrainFSM(StatesGroup):
    select_train_type = State()  # cardio or strength
    select_part = State()        # hand | body | leg
    select_train = State()       # squats, or push ups etc.
    complete = State()


async def is_state_complete(state: FSMContext):
    current_state = await state.get_state()
    return current_state == TrainFSM.complete


class TrainFSMAdapter:
    def __init__(self, state: FSMContext, callback_data: str):
        self._state = state
        self._callback_data = callback_data

    def is_cardio(self) -> bool:
        return self._callback_data == TRAIN_TYPE_CARDIO



    async def next(self) -> str:
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

    async def prev(self) -> str:
        state = await self._state.get_state()
        if state == TrainFSM.select_train_type:
            await self._state.update_data(part=None, train=None, train_type=None)
            await self._state.set_state(None)
        if state == TrainFSM.select_part:
            await self._state.update_data(part=None, train=None)
            await self._state.set_state(TrainFSM.select_train_type)
        if state == TrainFSM.select_train:
            if not self.is_cardio():
                await self._state.update_data(train=None)
                await self._state.set_state(TrainFSM.select_part)
            else:
                await self._state.update_data(part=None, train=None)
                await self._state.set_state(TrainFSM.select_train_type)
        if state == TrainFSM.complete:
            await self._state.update_data(train=None)
            await self._state.set_state(TrainFSM.select_train)

        return await self._state.get_state()


async def resolve_message_and_markup(current_state, state):
    match current_state:
        case TrainFSM.select_train_type.state:
            msg = 'Тип тренировки?'
            markup = kb.get_train_type()
        case TrainFSM.select_part.state:
            msg = 'На какую часть?'
            markup = kb.get_parts()
        case TrainFSM.select_train.state:
            msg = 'Какая тренировка?'
            state_data = await state.get_data()
            train_type = state_data.get('train_type')
            part = state_data.get('part')
            exercises = await Exercise.filter_by_train_type_and_part(train_type, part)
            markup = kb.render_exercise(exercises)
        case TrainFSM.complete.state:
            msg = 'Добавить `подход {вес} {кол-во раз}`\n для завершение `готово`'
            markup = None
        case _:
            msg = 'На главное меню.'
            markup = kb.main
    return msg, markup
