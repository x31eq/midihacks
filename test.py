import midi

if __name__ == '__main__':
    for s, m in [
            (0x80, 2), (0x91, 2), (0xa2, 2), (0xa3, 2),
            (0xb4, 2), (0xc5, 1), (0xd6, 1), (0xe7, 2),
            (0x88, 2), (0x89, 2), (0x8a, 2), (0x8b, 2),
            (0x8c, 2), (0x8d, 2), (0x8e, 2), (0x8f, 2),
            ]:
        assert midi.data_bytes(s) == m
