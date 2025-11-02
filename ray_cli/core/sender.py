from abc import ABC, abstractmethod
from typing import Sequence


class Sender(ABC):

    @abstractmethod
    def open(self): ...

    @abstractmethod
    def close(self): ...

    @abstractmethod
    def send(self, dmx_data: Sequence[int]): ...

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
