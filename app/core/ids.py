import os
import time
import uuid

def new_id() -> uuid.UUID:
    """A version 7 UUID: 6 bytes of time (in milliseconds), then 10 random bytes."""
    time_part = int(time.time() * 1000).to_bytes(6, "big")
    random_part = bytearray(os.urandom(10))
    random_part[0] = (random_part[0] & 0x0F) | 0x70  # the first digit of the third group becomes 7: the version
    random_part[2] = (random_part[2] & 0x3F) | 0x80  # two marker bits that say: a standard UUID
    return uuid.UUID(bytes=time_part + bytes(random_part))