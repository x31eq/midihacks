try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from machine import UART, Pin

class ESPStream(retune.Retuner):
    def output(self, mess):
        self.uart.write(bytes(mess))

def exit_event(p):
    global loop
    loop = False


def main():
    exit_pin = Pin(15, Pin.IN)
    exit_pin.irq(trigger=Pin.IRQ_FALLING, handler=exit_event)
    loop = True
    midistream = ESPStream()

    try:
        midistream.uart = UART(0, 31250)
        midistream.uart.init(31250)
        while loop:
            mess = midistream.uart.read(4)
            if mess:
                midistream.add_bytes(mess)
    except Exception as e:
        esp_fail = e
        raise
    finally:
        midistream.uart.init(115200)
