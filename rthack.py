import rtmidi
import sys

import retune

class RTStream(retune.Retuner):
    def output(self, mess):
        midiout.sendMessage(rtmidi.MidiMessage(bytes(mess)))

midiin = rtmidi.RtMidiIn()
if len(sys.argv) > 1:
    instr = sys.argv[1]
    inport = next(i for i in range(midiin.getPortCount())
            if instr in midiin.getPortName(i))
    midiin.openPort(inport)
else:
    midiin.openVirtualPort()

midiout = rtmidi.RtMidiOut()
if len(sys.argv) > 2:
    outstr = sys.argv[2]
    outport = next(i for i in range(midiout.getPortCount())
            if outstr in midiout.getPortName(i))
    midiout.openPort(outport)
else:
    midiout.openVirtualPort()

midistream = RTStream()
midistream.midiout = midiout

while True:
    mess = midiin.getMessage()
    if mess is not None:
        midistream.add_bytes(mess.getRawData())
