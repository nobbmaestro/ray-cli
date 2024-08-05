import pytest

from ray_cli.modes import RampModeOutputGenerator
from ray_cli.modes.generators import (
    ChaseModeOutputGenerator,
    RampDownModeOutputGenerator,
    RampUpModeOutputGenerator,
    SineModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
)


@pytest.mark.parametrize("fps, expected", [
    (4,  [[10]] * 4),
    (6,  [[10]] * 6),
    (10, [[10]] * 10),
])  # fmt: skip
def test_static_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = StaticModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (4,  [[0], [4], [4], [0]]),
    (6,  [[0], [2], [4], [4], [2], [0]]),
    (10, [[0], [1], [2], [3], [4], [4], [3], [2], [1], [0]]),
])  # fmt: skip
def test_ramp_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=4):
    generator = RampModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [4]]),
    (5,  [[0], [1], [2], [3], [4]]),
    (9,  [[0], [1], [1], [2], [2], [3], [3], [4], [4]]),
])  # fmt: skip
def test_ramp_up_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=4):
    generator = RampUpModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[4], [0]]),
    (5,  [[4], [3], [2], [1], [0]]),
    (9,  [[4], [4], [3], [3], [2], [2], [1], [1], [0]]),
])  # fmt: skip
def test_ramp_down_mode_output_shape(
    fps, expected, channels=1, frequency=1, intensity=4
):
    generator = RampDownModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (1,  [[10, 0, 0]]),
    (2,  [[10, 0, 0], [0, 0, 10]]),
    (3,  [[10, 0, 0], [0, 10, 0], [0, 0, 10]]),
    (6,  [[10, 0, 0], [10, 0, 0], [0, 10, 0], [0, 10, 0], [0, 0, 10], [0, 0, 10]]),
])  # fmt: skip
def test_chase_mode_output_shape(fps, expected, channels=3, frequency=1, intensity=10):
    generator = ChaseModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            output = next(generator)
            assert output == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [10]]),
    (4,  [[0], [0], [10], [10]]),
    (8,  [[0], [0], [0], [0], [10], [10], [10], [10]]),
])  # fmt: skip
def test_square_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = SquareModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("fps, expected", [
    (2,  [[0], [10]]),
    (4,  [[0], [9], [9], [1]]),
    (8,  [[0], [5], [8], [10], [10], [8], [5], [1]]),
])  # fmt: skip
def test_sine_mode_output_shape(fps, expected, channels=1, frequency=1, intensity=10):
    generator = SineModeOutputGenerator(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    for _ in range(3):  # we run 3 cycles
        for i in expected:
            actual = next(generator)
            assert actual == i


@pytest.mark.parametrize("generator_class", [
    ChaseModeOutputGenerator,
    RampDownModeOutputGenerator,
    RampModeOutputGenerator,
    RampUpModeOutputGenerator,
    SineModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
])  # fmt: skip
@pytest.mark.parametrize("channels", [0, 1, 2, 3, 5, 10, 100, 512, 10000, 100000])
def test_channels_sweep(generator_class, channels, fps=6, frequency=1, intensity=10):
    generator = generator_class(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    actual = next(generator)

    assert len(actual) == channels


@pytest.mark.parametrize("generator_class", [
    ChaseModeOutputGenerator,
    RampDownModeOutputGenerator,
    RampModeOutputGenerator,
    RampUpModeOutputGenerator,
    SineModeOutputGenerator,
    SquareModeOutputGenerator,
    StaticModeOutputGenerator,
])  # fmt: skip
@pytest.mark.parametrize("intensity", [1, 2, 3, 5, 10, 100, 255])
def test_intensity_sweep(generator_class, intensity, channels=1, fps=6, frequency=1):
    generator = generator_class(
        channels=channels,
        fps=fps,
        frequency=frequency,
        intensity=intensity,
    )

    output = [next(generator) for _ in range(fps)]
    actual = max(
        i for sublist in output for i in sublist
    )  # find max value in the nested list

    assert pytest.approx(actual, abs=actual * 0.05) == intensity
