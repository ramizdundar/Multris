from enum import Enum


class Packet:
    name = "Unanimous"

    def __init__(self, packet_type, payload=None):
        self.packet_type = packet_type
        self.payload = payload


class PacketType(Enum):
    DISCOVER = 0
    RESPOND = 1
    QUIT = 2
    FIGURE = 3
