from dataclasses import dataclass
from typing import Tuple, ClassVar


@dataclass
class Boat:
    boats: ClassVar[list['boats']] = []
    position: list[Tuple[int, int]]
    direction: int
    tall: int
    sink: bool

    @classmethod
    def nb_boats(cls) -> int:
        return len(cls.boats)

    def __post_init__(self):
        Boat.boats.append(self)
