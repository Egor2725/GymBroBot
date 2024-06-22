

from app.database.train import Train, Exercise

from app.const import TRAIN_TYPE_STRENGTH, TRAIN_TYPE_CARDIO
from app.const import PART_BODY, PART_LEG, PART_HAND


_hand_exercises = ['поднятие на бицепс', 'разгибания на внут. головку трицепса',
                   'разгибания на внеш. головку трицепса', 'предплечья']
_body_exercises = ['жим', 'скручивания на пресс', 'плечи передние', 'плечи сред', 'плечи зад',
                   'поднятия на трапецию', 'тяга на широчайшую', 'тяга на ромбовидные', 'гиперэкстензия']
_leg_exercises = ['приседания', 'сгибания на бицепс бедра', 'разгибания на квадрицепс', 'ягодичный мост',
                  'разведение бёдер', 'сведение бёдер', 'икры']

_cardio_exercises = ["Бег", "Велосипед", "Гребля"]


async def load_exercise():
    # load STRENGTH exercises
    for exercise_name in _hand_exercises:
        await Exercise.get_or_create(exercise_name, TRAIN_TYPE_STRENGTH, PART_HAND)

    for exercise_name in _body_exercises:
        await Exercise.get_or_create(exercise_name, TRAIN_TYPE_STRENGTH, PART_BODY)

    for exercise_name in _leg_exercises:
        await Exercise.get_or_create(exercise_name, TRAIN_TYPE_STRENGTH, PART_LEG)
    # load Cardio exercises
    for exercise_name in _cardio_exercises:
        await Exercise.get_or_create(exercise_name, TRAIN_TYPE_CARDIO)






