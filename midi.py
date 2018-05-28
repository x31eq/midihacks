def data_bytes(status):
    msb = status >> 4
    assert msb & 8
    if msb == 0xf:
        # SysEx is still special
        return b'?\1\2\1\0\0\0\0\0\0\0\0\0\0\0\0'[status & 0xf]
    return b'\2\2\2\2\1\1\2'[msb & 7]
