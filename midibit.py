import midi

from microbit import button_a, sleep, uart, pin0, pin1

class BitStream(midi.Stream):
    def send_message(self, mess):
        uart.write(mess)

midistream = BitStream()

while not button_a.was_pressed():
    sleep(30)

try:
    uart.init(31250, tx=pin1, rx=pin0)
    while not button_a.was_pressed():
        midistream.add_bytes(uart.read(4))
finally:
    uart.init(115200)
