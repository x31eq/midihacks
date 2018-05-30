SysExStart = 0xf0
SysExEnd = 0xf7

class Stream:
    def __init__(self):
        self.in_stat = -1
        self.out_stat = -1
        self.data_wait = 0
        self.buf = []

    def add_bytes(self, dat):
        for val in dat:
            if val == SysExEnd:
                self.buf.append(val)
                self.send_buffer()
                self.buf = [SysExStart]
            elif val & 0x80:
                self.in_stat = val
                self.data_wait = data_bytes(val)
                self.buf = [val]
            elif self.in_stat == SysExStart:
                self.buf.append(val)
            elif self.data_wait:
                self.buf.append(val)
                self.data_wait -= 1
            else:
                self.data_wait = data_bytes(self.in_stat)
                if self.data_wait:
                    self.buf = [self.in_stat, val]
                    self.data_wait -= 1
            if not self.data_wait:
                self.send_buffer()
                self.data_wait = 0

    def send_message(self, mess):
        """
        Override this with your useful thing
        """
        print(''.join('%02x' % dat for dat in self.bytes_to_send(mess)))

    def send_buffer(self):
        assert self.buf
        if self.buf[0] == self.out_stat:
            self.send_message(self.buf[1:])
        else:
            if self.buf[0] < 0x90:
                self.out_stat =self.buf[0]
            else:
                self.out_stat = -1
            self.send_message(self.buf)


def data_bytes(status):
    msb = status >> 4
    assert msb & 8
    if msb == 0xf:
        # SysEx is still special
        return b'\1\1\2\1\0\0\0\0\0\0\0\0\0\0\0\0'[status & 0xf]
    return b'\2\2\2\2\1\1\2'[msb & 7]
