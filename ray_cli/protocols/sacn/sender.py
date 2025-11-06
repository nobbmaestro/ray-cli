import ipaddress
import itertools
import uuid
from typing import Optional, Sequence

from ray_cli.core import Sender

from .encoder import Encoder, SACNEncoder
from .sockets import (
    BaseUDPSocket,
    MulticastSocket,
    UnicastSocket,
    sacn_multicast_address,
)


class Universe:
    def __init__(
        self,
        encoder: Encoder,
        universe_nr: int,
        socket: BaseUDPSocket,
        priority: int,
    ):
        self._encoder = encoder
        self._universe_nr = universe_nr
        self._socket = socket
        self._priority = priority
        self._seq_nr_iter = itertools.cycle(range(256))

    def _next_sequence_nr(self):
        return next(self._seq_nr_iter)

    def open(self):
        self._socket.open()

    def close(self):
        self._socket.close()

    def send(self, dmx_data: Sequence[int]):
        self._socket.send(
            self._encoder.build_frame(
                universe=self._universe_nr,
                priority=self._priority,
                sequence=self._next_sequence_nr(),
                dmx_data=dmx_data,
            )
        )


class SACNSender(Sender):
    def __init__(
        self,
        source_name: str,
        universes: Sequence[int],
        priority: int = 100,
        src: ipaddress.IPv4Address = ipaddress.IPv4Address("0.0.0.0"),
        dst: Optional[ipaddress.IPv4Address] = None,
        cid: Optional[bytes] = None,
    ):
        self.priority = priority
        self.source_name = source_name
        self.cid = cid or uuid.uuid4().bytes

        if dst:
            self.universes = {
                u: Universe(
                    universe_nr=u,
                    priority=priority,
                    socket=UnicastSocket(bind_address=src, dest_address=dst),
                    encoder=SACNEncoder(cid=self.cid, source_name=self.source_name),
                )
                for u in universes
            }
        else:
            self.universes = {
                u: Universe(
                    universe_nr=u,
                    priority=priority,
                    socket=MulticastSocket(
                        bind_address=src,
                        group_address=sacn_multicast_address(u),
                    ),
                    encoder=SACNEncoder(cid=self.cid, source_name=self.source_name),
                )
                for u in universes
            }

    def open(self):
        for u in self.universes.values():
            u.open()

    def close(self):
        for u in self.universes.values():
            u.close()

    def send(self, dmx_data: Sequence[int]):
        for u in self.universes.values():
            u.send(dmx_data)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
