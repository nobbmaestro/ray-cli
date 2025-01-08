from typing import Sequence, Union

from .generators import (
    ChaseModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
)

DmxData = Sequence[int]

DmxDataGenerator = Union[
    SineModeDmxDataGenerator,
    SquareModeDmxDataGenerator,
    StaticModeDmxDataGenerator,
    RampModeDmxDataGenerator,
    RampUpModeDmxDataGenerator,
    RampDownModeDmxDataGenerator,
    ChaseModeDmxDataGenerator,
]
