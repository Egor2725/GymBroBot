from aiogram import types, Router
from aiogram.filters import CommandStart, Command

from aiogram.fsm.context import FSMContext

import keyboards as kb
from database.train import User


router = Router()


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
    await message.answer(f"Help message with all commands", reply_markup=kb.main)


@router.message()
async def handle_all_message(message: types.Message):
    await message.reply('Такой команды нет, /help для помощи.')
