try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from machine import UART, Pin

class ESPStream(retune.Retuner):
    def init_esp(self):
        self.loop = True
        self.midiout = UART(1, 31250)
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
        # An ESP8266 supports two UART buses:
        # 0 can send and receive
        # 1 can only send
        # Micropython uses bus 0 for the serial terminal,
        # so (on my board at least) UART can receive
        # on the RX pin but can't transmit on TX.
        # Bus 0 can, however, send on pin 2.
        # So, we need both buses.
        midiin = UART(0, 31250)
        midiin.init(31250)
        midistream.init_esp()
        while midistream.loop:
            mess = midiin.read(4)
            if mess:
                midistream.add_bytes(mess)
    except Exception as e:
        esp_fail = e
        raise
    finally:
        midiin.init(115200)
