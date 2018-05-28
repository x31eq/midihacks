def data_bytes(status):
    return b'\x02\x02\x02\x02\x01\x01\x02\x00'[status >> 4 & 7]
