import ipaddress
import itertools
import time
from typing import Iterator, Optional, Sequence

import sacn


class SACNDispatcher:
    def __init__(
        self,
        generator: Iterator,
        channels: int,
        fps: int,
        universes: Sequence[int],
        src_ip_address: ipaddress.IPv4Address,
    ):
        self.fps = fps
        self.channels = channels
        self.universes = universes
        self.generator = generator
        self.src_ip_address = src_ip_address
        self.sender = sacn.sACNsender(
            bind_address=str(self.src_ip_address),
            fps=self.fps,
        )

    @property
    def period(self):
        return 1 / self.fps

    def start(self):
        self.sender.start()
        for universe in self.universes:
            self.sender.activate_output(universe)
            self.sender[universe].multicast = True
        self.sender.manual_flush = True

    def stop(self):
        self.sender.stop()

    def run(
        self,
        duration: Optional[int] = None,
    ):
        self.start()

        num_frames = (
            range(round(self.fps * duration)) if duration else itertools.count(0, 1)
        )

        for _ in num_frames:
            t_0 = time.perf_counter()

            payload = next(self.generator)
            for universe in self.universes:
                self.sender[universe].dmx_data = payload
            self.sender.flush()
            elapsed_time = time.perf_counter() - t_0
            t_sleep = max(0, self.period - elapsed_time)
            time.sleep(t_sleep)

        self.stop()
