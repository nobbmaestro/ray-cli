import ipaddress
import logging
import socket
from dataclasses import dataclass
from typing import Optional, Sequence

import sacn

logger = logging.getLogger(__name__)

ACN_SDT_MULTICAST_PORT = 5568

VECTOR_ROOT_E131_EXTENDED = (00, 00, 00, 0x08)

_FIRST_INDEX = (
    0,
    0x10,
    0,
    0,
    0x41,
    0x53,
    0x43,
    0x2D,
    0x45,
    0x31,
    0x2E,
    0x31,
    0x37,
    0x00,
    0x00,
    0x00,
)


@dataclass
class RootLayer:
    cid: int
    length: int
    vector: tuple = VECTOR_ROOT_E131_EXTENDED

    def to_bytes(self) -> bytes:
        return b""


@dataclass
class DataPacket:
    source_name: str
    priority: int
    sync_addr: int
    universe: int
    option_stream_terminated: bool
    option_preview_data: bool
    option_force_sync: bool
    sequence: int
    dmx_start_code: int
    dmx_data: tuple

    def to_bytes(self) -> bytes:
        return b""


class Packet:
    root_layer: RootLayer
    data_packet: DataPacket


class SACNSocket:
    def __init__(
        self,
        address: ipaddress.IPv4Address,
        port: int = 5568,
    ):
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, to: ipaddress.IPv4Address, data):
        self.socket.sendto(data, (str(to), ACN_SDT_MULTICAST_PORT))

    def broadcast(self, data):
        raise NotImplementedError()

    def start(self):
        self.socket.bind((self.address, ACN_SDT_MULTICAST_PORT))

    def stop(self):
        self.socket.close()

    def __enter__(self):
        self.start()

    def __exit__(self, type_, value, traceback):
        self.stop()


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
