class Stream:
    def __init__(self):
        self.in_stat = -1
        self.data_wait = 0
        self.buf = b''

    def add_byte(self, dat):
        val = dat[0]
        if val == b'\xf7':
            self.send_message(self.buf + val)
            self.buf = b'\xf0'
        elif val & 0x80:
            self.in_stat = dat
            self.data_wait = data_bytes(val)
            self.buf = dat
        elif self.in_stat == b'\xf0':
            self.buf += dat
        elif self.data_wait:
            self.buf += dat
            self.data_wait -= 1
        else:
            self.data_wait = data_bytes(self.in_stat[0])
            if self.data_wait:
                self.buf = self.in_stat + dat
                self.data_wait -= 1
        if not self.data_wait:
            self.send_message(self.buf)
            self.data_wait = 0

    def send_message(self, mess):
        """
        Override this with your useful thing
        """
        print(''.join(f'{dat:02x}' for dat in mess))


def data_bytes(status):
    msb = status >> 4
    assert msb & 8
    if msb == 0xf:
        # SysEx is still special
        return b'\1\1\2\1\0\0\0\0\0\0\0\0\0\0\0\0'[status & 0xf]
    return b'\2\2\2\2\1\1\2'[msb & 7]
