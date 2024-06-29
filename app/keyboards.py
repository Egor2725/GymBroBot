from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from const import TRAIN_TYPES
from const import PARTS
from data import get_train_by


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать тренировку", callback_data='add_train')],
    [InlineKeyboardButton(text="История тренировок", callback_data='history')],
    [InlineKeyboardButton(text="Рекомендации", callback_data='recommends')],
    [InlineKeyboardButton(text="Отчет", callback_data='report')],
])


def get_train_type():
    keyboards = [
        [InlineKeyboardButton(text=train_type.capitalize(), callback_data=f'add_train{train_type}')]
        for train_type in TRAIN_TYPES
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def get_parts():
    keyboards = [
        [InlineKeyboardButton(text=part.capitalize(), callback_data=f'add_train{part}')]
        for part in PARTS
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def get_train(train_type, part):
    trains = get_train_by(train_type, part)

    keyboards = [
        [InlineKeyboardButton(text=train.name.capitalize(), callback_data=f'add_train{train.id}')]
        for train in trains
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboards)

