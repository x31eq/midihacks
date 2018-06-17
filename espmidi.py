try:
    import retune
except ImportError:
    import sys
    sys.exit(0)

from machine import UART, Pin

class ESPStream(retune.Retuner):
    def output(self, mess):
        self.midiout.write(bytes(mess))

def exit_event(p):
    global loop
    loop = False

loop = True

def main():
    exit_pin = Pin(15, Pin.IN)
    exit_pin.irq(trigger=Pin.IRQ_FALLING, handler=exit_event)
    midistream = ESPStream()

    try:
        midiin = UART(0, 31250)
        midiin.init(31250)
        midistream.midiout = UART(1, 31250)
        midistream.midiout.init(31250)
        while loop:
            mess = midiin.read(4)
            if mess:
                midistream.add_bytes(mess)
    except Exception as e:
        esp_fail = e
        raise
    finally:
        midiin.init(115200)
