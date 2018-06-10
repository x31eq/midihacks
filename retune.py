import midi

class Retuner(midi.Stream):
    def hack(self, mess):
        if not hasattr(self, 'channel_for_key'):
            self.channel_for_key = bytearray(0x80)

        if mess[0] & 0xef == 0x80:
            key = mess[1]
            pitch = (key - 60) * 12 / 29 + 60
            note = round(pitch)
            note = min(max(note, 0), 0x7f)
            if mess[0] == 0x80 and mess[2]:
                self.chan = (getattr(self, 'chan', -1) + 1) & 7
                chan = self.chan
                self.channel_for_key[key] = chan
                bend = round((pitch - note + 2) * 0x80 * 0x80 / 4) & 0x3fff
                result = [(0xe0 + chan, bend & 0x7f, bend >> 7)]
            else:
                chan = self.channel_for_key[key]
                result = []
            return result + [(mess[0] + chan, note, mess[2])]

        return [mess]
