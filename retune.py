import midi

class Retuner(midi.Out):
    def hack(self, mess):
        if not hasattr(self, 'channel_for_key'):
            self.channel_for_key = bytearray(0x80)

        if mess[0] & 0xef == 0x80:
            key = mess[1]
            pitch = (key - 60) * 12 / 29 + 60
            note = round(pitch)
            note = min(max(note, 0), 0x7f)
            if mess[0] == 0x90 and mess[2]:
                self.chan = (getattr(self, 'chan', -1) + 1) & 7
                chan = self.chan
                self.channel_for_key[key] = chan
                bend = round((pitch - note + 2) * 0x80 * 0x80 / 4) & 0x3fff
                yield 0xe0 + chan, bend & 0x7f, bend >> 7
            else:
                chan = self.channel_for_key[key]
            yield mess[0] + chan, note, mess[2]
        elif mess[0] & 0xf0 < 0xf0 and mess[0] & 0xf == 0:
            for chan in range(8):
                yield [mess[0] + chan] + list(mess[1:])
        else:
            yield mess
