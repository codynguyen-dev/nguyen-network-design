import struct

_HEADER_FMT = "!IH"
_HEADER_SIZE = struct.calcsize(_HEADER_FMT)

def make_packet(seq: int, payload: bytes) -> bytes:
    if not (0 <= seq <= 0xFFFFFFFF):
        raise ValueError("seq out of range")
    if len(payload) > 1024:
        raise ValueError("payload too large (>1024)")
    header = struct.pack(_HEADER_FMT, seq, len(payload))
    return header + payload

def parse_packet(pkt: bytes) -> tuple[int, bytes]:
    if len(pkt) < _HEADER_SIZE:
        raise ValueError("packet too short")
    seq, length = struct.unpack(_HEADER_FMT, pkt[:_HEADER_SIZE])
    payload = pkt[_HEADER_SIZE:_HEADER_SIZE + length]
    if len(payload) != length:
        raise ValueError("payload length mismatch")
    return seq, payload