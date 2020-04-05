import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 2

fig, (ax2) = plt.subplots(1, figsize=(15,8))


x = np.arange(0, 2*CHUNK, 2)

#space in between points represents RATE/CHUNK Hz = 21.53 Hz interval
x_fft = np.linspace(0,RATE, CHUNK)

line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)
ax2.set_xlim(20, RATE/2)
plt.show(block=False)
LOW_FREQ = 100 #100*21.53 = 2153 HZ
HI_FREQ = 500 #500*21.53 = 10765 Hz
interval = RATE/CHUNK

stream = mic.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)
while True:
    data = stream.read(CHUNK)
    data_int = struct.unpack(str(2*CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2] + 128
    y_fft = fft(data_int)
    magnitude = np.abs(y_fft[0:CHUNK])*2/(256 *CHUNK)
    subfrequencies = magnitude[100:500]
    line_fft.set_ydata(magnitude)
    max_freq = np.argmax(subfrequencies)

    print("max freq occurs at: %f, %f" % ((max_freq + 100) * interval, subfrequencies[max_freq]))
    fig.canvas.draw()
    fig.canvas.flush_events()


