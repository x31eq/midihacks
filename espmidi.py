try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from machine import UART, Pin

class ESPStream(retune.Retuner):
    def init_esp(self):
        self.loop = True
        self.midiout = UART(0, 31250)
        self.midiout.init(31250)
        exit_pin = Pin(15, Pin.IN)
        exit_pin.irq(
                trigger=Pin.IRQ_FALLING,
                handler=self.exit_event)

    def output(self, mess):
        self.midiout.write(bytes(mess))

    def exit_event(self, p):
        self.loop = False


def main():
    midistream = ESPStream()

    try:
        midistream.init_esp()
        midiin = midistream.midiout
        while midistream.loop:
            mess = midiin.read(4)
            if mess:
                midistream.add_bytes(mess)
    finally:
        midiin.init(115200)
