import itertools
import time
from typing import Optional, Union

from ray_cli.dispatchers import SACNDispatcher
from ray_cli.modes import (
    ChaseModeOutputGenerator,
    RampModeOutputGenerator,
    StaticModeOutputGenerator,
)
from ray_cli.utils import Feedback, ProgressBar, TableLogger


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

        self.table_logger = TableLogger(channels)
        self.progress_bar = ProgressBar(round(fps * duration) if duration else None)

    def run(
        self,
        feedback: Optional[Feedback] = None,
        dry=False,
    ):
        self.dispatcher.start()

        t_start = time.time()

        num_frames = (
            range(round(self.fps * self.duration))
            if self.duration
            else itertools.count(0, 1)
        )

        for i in num_frames:
            t_0 = time.perf_counter()

            payload = next(self.generator)
            if not dry:
                self.dispatcher.send(payload)

            if feedback == Feedback.TABULAR:
                self.table_logger.report(i + 1, payload)

            elif feedback == Feedback.PROGRESS_BAR:
                self.progress_bar.report(
                    i + 1,
                    time.time() - t_start,
                )

            elapsed_time = time.perf_counter() - t_0
            t_sleep = max(0, 1 / self.fps - elapsed_time)
            time.sleep(t_sleep)

        self.dispatcher.stop()
