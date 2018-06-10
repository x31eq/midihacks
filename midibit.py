try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from microbit import button_a, sleep, uart, pin0, pin1
from microbit import display, Image

class BitStream(retune.Retuner):
    def output(self, mess):
        uart.write(bytes(mess))

midistream = BitStream()

while not button_a.was_pressed():
    sleep(30)

try:
    uart.init(31250, tx=pin1, rx=pin0)
    display.show(Image.NO)
    while not button_a.was_pressed():
        mess = uart.read(4)
        if mess:
            display.show(Image.MUSIC_CROTCHET)
            midistream.add_bytes(mess)
except Exception as e:
    midibit_fail = e
finally:
    uart.init(115200)
