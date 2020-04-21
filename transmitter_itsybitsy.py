"""import time
import audioio
import board
import digitalio
 
wave_file = open("laugh.wav", "rb")
wave = audioio.WaveFile(wave_file)
audio = audioio.AudioOut(board.A0)
 
while True:
    audio.play(wave)
 
    # This allows you to do other things while the audio plays!
    t = time.monotonic()
    while time.monotonic() - t < 6:
        pass
 
    while audio.playing:
        pass
    print("Done!")

"""

import time
import array
import math
import audioio
import board
import digitalio
from analogio import AnalogIn
 
signal_to_send = [0,1,0,0,1,1,0,1,1,0,0]
signal_length = 2

tone_volume = 1  # Increase this to increase the volume of the tone.
lfrequency = 1050  # Set this to the Hz of the tone you want to generate.
llength = 8000 // lfrequency
low_freq_wave = array.array("H", [0] * llength)
for i in range(llength):
    low_freq_wave[i] = int((1 + math.sin(math.pi * 2 * i / llength)) * tone_volume * (2 ** 15 - 1))

frequency = 1600  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency
high_freq_wave = array.array("H", [0] * length)
for i in range(length):
    high_freq_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))
 
#audio = audioio.AudioOut(board.A0, board.A0)
#low_freq_wave_sample = audioio.RawSample(low_freq_wave)

f = open("laugh.wav", "rb")
a = audioio.AudioOut(board.A0, f)


analog_in = AnalogIn(board.A1)
i = 0
while True:
  #print(analog_in.value)
  if(signal_to_send[i]==1):
    a = audioio.AudioOut(board.A0, high_freq_wave)
    print("playing")
    a.play(loop=True)
    time.sleep(signal_length/2)
    a.stop()
    time.sleep(signal_length/2)
  else:
    a = audioio.AudioOut(board.A0, low_freq_wave)
    print("playing")
    a.play(loop=True)
    time.sleep(signal_length/2)
    a.stop()
    time.sleep(signal_length/2)
    while a.playing:
      pass
    print("stopped")
  i+= 1
  if(i>=len(signal_to_send)):
    i = 0
  
