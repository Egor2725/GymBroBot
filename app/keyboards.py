from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.const import TRAIN_TYPES
from app.const import PARTS


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать тренировку", callback_data='add_train')],
    [InlineKeyboardButton(text="История тренировок", callback_data='history')],
    [InlineKeyboardButton(text="Рекомендации", callback_data='recommends')],
    [InlineKeyboardButton(text="Отчет", callback_data='report')],
])

_back = [InlineKeyboardButton(text="Назад", callback_data=f'add_train_back')]
back = InlineKeyboardMarkup(inline_keyboard=[_back])


def get_train_type():
    keyboards = [
        [InlineKeyboardButton(text=train_type.capitalize(), callback_data=f'add_train{train_type}')]
        for train_type in TRAIN_TYPES
    ]
    keyboards.append(_back)
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def get_parts():
    keyboards = [
        [InlineKeyboardButton(text=part.capitalize(), callback_data=f'add_train{part}')]
        for part in PARTS
    ]
    keyboards.append(_back)
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def render_exercise(exercises):
    keyboards = [
        [InlineKeyboardButton(text=exercise.name.capitalize(), callback_data=f'add_train{exercise.id}')]
        for exercise in exercises
    ]
    keyboards.append(_back)
    return InlineKeyboardMarkup(inline_keyboard=keyboards)

