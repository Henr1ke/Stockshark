from enum import Enum, auto


class State(Enum):
    IN_PROGRESS = auto()
    DRAW = auto()
    WIN_W = auto()
    WIN_B = auto()
