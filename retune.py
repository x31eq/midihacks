import midi

class Retuner(midi.Stream):
    def hack(self, mess):
        if not hasattr(self, 'channel_for_note'):
            self.channel_for_note = bytearray(0x80)

        if mess[0] & 0xef == 0x80:
            pitch = (mess[1] - 60) * 12 / 29 + 60
            note = round(pitch)
            note = min(max(note, 0), 0x7f)
            if mess[0] == 0x80 and mess[2]:
                self.chan = (getattr(self, 'chan', -1) + 1) & 7
                chan = self.chan
                self.channel_for_note[note] = chan
                bend = round((pitch - note + 2) * 0x80 * 0x80 / 4) & 0x3fff
                result = [(0xe0 + chan, bend & 0x7f, bend >> 7)]
            else:
                chan = self.channel_for_note[note]
                result = []
            return result + [(mess[0] + chan, note, mess[2])]

        return [mess]
