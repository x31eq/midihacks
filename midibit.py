try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from microbit import button_a, sleep, uart, pin1, pin2
from microbit import display, Image

class BitOut(retune.Retuner):
    def output(self, mess):
        uart.write(bytes(mess))

midistream = BitOut()
display.show(Image.HAPPY)

while not button_a.was_pressed():
    sleep(30)

try:
    uart.init(31250, tx=pin2, rx=pin1)
    display.show(Image.NO)
    while not button_a.was_pressed():
        mess = uart.read(4)
        if mess:
            display.show(Image.MUSIC_CROTCHET)
            midistream.write(mess)
except Exception as e:
    midibit_fail = e
    raise
finally:
    uart.init(115200)

display.show(Image.YES)
