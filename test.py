from unittest import mock

import midi

if __name__ == '__main__':
    for s, m in [
            (0x80, 2), (0x91, 2), (0xa2, 2), (0xa3, 2),
            (0xb4, 2), (0xc5, 1), (0xd6, 1), (0xe7, 2),
            (0x88, 2), (0x89, 2), (0x8a, 2), (0x8b, 2),
            (0x8c, 2), (0x8d, 2), (0x8e, 2), (0x8f, 2),
            (0xf0, 1), (0xf1, 1), (0xf2, 2), (0xf3, 1),
            (0xf4, 0), (0xf5, 0), (0xf6, 0),
            (0xf8, 0), (0xf9, 0), (0xfa, 0), (0xfb, 0),
            (0xfc, 0), (0xfd, 0), (0xfe, 0), (0xff, 0),
            ]:
        assert midi.data_bytes(s) == m, f'Wrong data size for 0x{s:02x}'

    s = midi.Stream()
    with mock.patch.object(s, 'send_message') as send:
        s.add_byte(b'\x80')
        s.add_byte(b'\x10')
        s.add_byte(b'\x20')
        send.assert_called_once_with(b'\x80\x10\x20')
        send.reset_mock()
        s.add_byte(b'\x30')
        s.add_byte(b'\x40')
        send.assert_called_once_with(b'\x80\x30\x40')
