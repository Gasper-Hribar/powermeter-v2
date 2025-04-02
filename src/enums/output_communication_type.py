
# ENUMS for output communication type
from enum import Enum, auto

class EOutputCommunicationType(Enum):
    RASPBERRY_PI = auto()
    DUMMY = auto()
    INVALID = auto()
    