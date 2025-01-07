from typing import Union

from .generators import (
    ChaseModeOutputGenerator,
    RampDownModeOutputGenerator,
    RampModeOutputGenerator,
    RampUpModeOutputGenerator,
    SineModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
)

Generator = Union[
    SineModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
    RampModeOutputGenerator,
    RampUpModeOutputGenerator,
    RampDownModeOutputGenerator,
    ChaseModeOutputGenerator,
]
