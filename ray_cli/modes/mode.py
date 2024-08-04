import enum


class Mode(str, enum.Enum):
    CHASE = "chase"
    RAMP = "ramp"
    RAMP_DOWN = "ramp-down"
    RAMP_UP = "ramp-up"
    SQUARE = "square"
    STATIC = "static"
