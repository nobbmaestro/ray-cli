import enum


class Mode(str, enum.Enum):
    STATIC = "static"
    CHASE = "chase"
    RAMP = "ramp"
