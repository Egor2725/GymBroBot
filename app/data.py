# imitation of db module remove in future
from const import TRAIN_TYPE_STRENGTH
from const import PART_HAND, PART_BODY, PART_LEG
from dataclasses import dataclass


@dataclass
class Train:
    id: int
    name: str

    def __str__(self):
        return f'Упраженение: {self.name}'


trains_list = [
    Train(id=i, name=name)
    for i, name in enumerate(
        (
            "Бицепс с гантелями", "Трицепс с гантелями",
             "Пресс", "Жим от груди",
             "Приседания", "Икры"
         ))
]

trains = {
    PART_HAND: trains_list[:2],
    PART_BODY: trains_list[2:4],
    PART_LEG: trains_list[4:],
}


def get_train_by(train_type, part):
    if train_type == TRAIN_TYPE_STRENGTH:
        return trains[part]

    else:
        # cardio
        return [Train(id=ident+100, name=name) for ident, name in enumerate(["Бег", "Велосипед", "Гребля"])]


def get_train_by_id(index):
    return trains_list[int(index)]
