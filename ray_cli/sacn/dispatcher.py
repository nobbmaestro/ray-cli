import ipaddress
import logging
from typing import Optional, Sequence

import sacn

logger = logging.getLogger(__name__)


class SACNDispatcher:
    def __init__(
        self,
        channels: int,
        fps: int,
        universes: Sequence[int],
        src_ip_address: ipaddress.IPv4Address,
        dst_ip_address: Optional[ipaddress.IPv4Address] = None,
    ):
        self.fps = fps
        self.channels = channels
        self.universes = universes
        self.src_ip_address = src_ip_address
        self.dst_ip_address = dst_ip_address

        self.sender = sacn.sACNsender(
            bind_address=str(self.src_ip_address),
            fps=self.fps,
        )

    def start(self):
        self.sender.start()
        for universe in self.universes:
            self.sender.activate_output(universe)
            if self.dst_ip_address:
                self.sender[universe].destination = str(self.dst_ip_address)
            else:
                self.sender[universe].multicast = True
        self.sender.manual_flush = True

    def stop(self):
        self.sender.stop()

    def send(self, payload):
        for universe in self.universes:
            self.sender[universe].dmx_data = payload
        self.sender.flush()
