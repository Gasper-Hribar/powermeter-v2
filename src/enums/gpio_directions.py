
# ENUMS for output communication type
from enum import Enum, auto

class EGPIO_Direction(Enum):
    OUTPUT = auto()
    INPUT = auto()

class EGPIO_Output(Enum):
    HIGH = 1
    LOW = 0

    