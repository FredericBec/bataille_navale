from dataclasses import dataclass
from typing import Tuple, ClassVar


@dataclass
class Boat:
    position: list[Tuple[int, int]]
    direction: int
    tall: int
    sink: bool
