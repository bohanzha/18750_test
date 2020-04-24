import time
import array
import math
import audioio
import board
import digitalio
from analogio import AnalogIn
import hamming

tone_volume = 1  # Increase this to increase the volume of the tone.
# 1593 Hz
lfrequency = 1500  # Set this to the Hz of the tone you want to generate.
llength = 8000 // lfrequency
low_freq_wave = array.array("H", [0] * llength)
for i in range(llength):
    low_freq_wave[i] = int((1 + math.sin(math.pi * 2 * i / llength)) * tone_volume * (2 ** 15 - 1))

frequency = 2100  # Set this to the Hz of the tone you want to generate.
# 2670 Hz
length = 8000 // frequency
high_freq_wave = array.array("H", [0] * length)
for i in range(length):
    high_freq_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))

analog_in = AnalogIn(board.A1)
a = audioio.AudioOut(board.A0)
pulse_width = 0.3
sine_wave_sample_hi = audioio.RawSample(high_freq_wave)
sine_wave_sample_lo = audioio.RawSample(low_freq_wave)

while True:
    print("transmit:")
    transmission = input()
    print("transmitting '%s'" % transmission)
    for c in transmission:
        print("byte: %c" % c)
        frame = hamming.generate_hamming_frame(c)
        print(frame)
        for m in frame:
            if m == 1:
                a.play(sine_wave_sample_hi, loop=True)
            else:
                a.play(sine_wave_sample_lo, loop=True)
            time.sleep(pulse_width)
            a.stop()
            time.sleep(0.2)
