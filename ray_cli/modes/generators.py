import itertools
from abc import ABC, abstractmethod
from typing import Iterator, List


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
