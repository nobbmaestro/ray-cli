import itertools
import math
from abc import ABC, abstractmethod
from typing import Iterator, List

import numpy


class BaseGenerator(ABC):
    def __init__(
        self,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ):
        super().__init__()
        self.channels = channels
        self.fps = fps
        self.frequency = frequency
        self.intensity = intensity
        self.generator = self.create(channels, fps, frequency, intensity)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    @abstractmethod
    def next(self) -> List[int]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        raise NotImplementedError()


class StaticModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [output_coeff for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        return itertools.cycle([intensity])


class RampModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [math.ceil(output_coeff * self.intensity) for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil((fps / frequency) / 2)
        return itertools.cycle(
            itertools.chain(
                numpy.linspace(0, 1, size),
                numpy.linspace(1, 0, size),
            ),
        )


class RampUpModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [math.ceil(output_coeff * self.intensity) for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(
            itertools.chain(
                numpy.linspace(0, 1, size),
            ),
        )


class RampDownModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [math.ceil(output_coeff * self.intensity) for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(
            itertools.chain(
                numpy.linspace(1, 0, size),
            ),
        )


class ChaseModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        channel = round(next(self.generator))
        return [self.intensity if channel == i else 0 for i in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)
        return itertools.cycle(numpy.linspace(0, channels - 1, size))


class SquareModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [math.ceil(output_coeff * self.intensity) for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil((fps / frequency) / 2)
        return itertools.cycle(
            itertools.chain(
                numpy.linspace(0, 0, size),
                numpy.linspace(1, 1, size),
            ),
        )


class SineModeOutputGenerator(BaseGenerator):

    def next(self) -> List[int]:
        output_coeff = next(self.generator)
        return [math.ceil(output_coeff * self.intensity) for _ in range(self.channels)]

    @classmethod
    def create(
        cls,
        channels: int,
        fps: int,
        frequency: float,
        intensity: int,
    ) -> Iterator:
        size = math.ceil(fps / frequency)

        if size <= 2:
            return itertools.cycle([0, 1])

        x_values = numpy.linspace(0, numpy.pi, size)
        return itertools.cycle(itertools.chain(numpy.sin(x_values)))
