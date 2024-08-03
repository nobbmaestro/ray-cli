import enum


class Mode(str, enum.Enum):
    CHASE = "chase"
    RAMP = "ramp"
    RAMP_UP = "ramp-up"
    STATIC = "static"
