import midi

class Retuner(midi.stream):
    def hack(self, mess):
        if mess[0] & 0xef == 0x80:
            pitch = (mess[1] - 60) * 12 / 29 + 60
            note = round(pitch)
            note = min(max(note, 0), 0x7f)
            if mess[0] == 0x80 and mess[2]:
                bend = round((pitch - note) * 0x80 * 0x80 / 4) & 0x3fff
                result = [(0xe0, bend & 0x7f, bend >> 7)]
            else:
                result = []
            return result + [(mess[0], note, mess[2])]

