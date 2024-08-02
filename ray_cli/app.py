import itertools
import time
from typing import Optional, Union

from ray_cli.modes import (
    ChaseModeOutputGenerator,
    RampModeOutputGenerator,
    StaticModeOutputGenerator,
)
from ray_cli.sacn.dispatcher import SACNDispatcher


class App:
    def __init__(
        self,
        dispatcher: SACNDispatcher,
        generator: Union[
            ChaseModeOutputGenerator,
            RampModeOutputGenerator,
            StaticModeOutputGenerator,
        ],
        channels: int,
        fps: int,
        duration: Optional[int] = None,
    ):
        self.dispatcher = dispatcher
        self.generator = generator
        self.channels = channels
        self.fps = fps
        self.duration = duration

    def run(self):
        self.dispatcher.start()

        num_frames = (
            range(round(self.fps * self.duration))
            if self.duration
            else itertools.count(0, 1)
        )

        for _ in num_frames:
            t_0 = time.perf_counter()

            payload = next(self.generator)
            self.dispatcher.send(payload)

            elapsed_time = time.perf_counter() - t_0
            t_sleep = max(0, 1 / self.fps - elapsed_time)
            time.sleep(t_sleep)

        self.dispatcher.stop()
