import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft
import filter
from scipy import signal

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 2
SHORT_NORMALIZE = (1.0/32768.0)

def design_filter(lowcut, highcut, fs, order=3):
    nyq = 0.5*fs
    low = lowcut/nyq
    high = highcut/nyq
    b,a = signal.butter(order, [low,high], btype='band')
    return b,a

def normalize(block):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )
    doubles = [x * SHORT_NORMALIZE for x in shorts]
    return doubles


def get_rms(samples):
    sum_squares = 0.0
    for sample in samples:
        sum_squares += sample*sample
    return np.sqrt( sum_squares / len(samples) )

#fig, (ax2) = plt.subplots(1, figsize=(15,8))


#x = np.arange(0, 2*CHUNK, 2)

#space in between points represents RATE/CHUNK Hz = 21.53 Hz interval
#x_fft = np.linspace(0,RATE, CHUNK)

#line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)
#ax2.set_xlim(20, RATE/2)
#plt.show(block=False)
LOW_FREQ = 100 #100*21.53 = 2153 HZ
HI_FREQ = 500 #500*21.53 = 10765 Hz
interval = RATE/CHUNK

b,a = design_filter(500, 1000, RATE)
zi = signal.lfilter_zi(b,a)

stream = mic.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)
while True:
    data = stream.read(CHUNK)
    samples = normalize(data)
    bandpass_samples, zi = signal.lfilter(b,a,np.array(samples), zi=zi)
    amplitude = get_rms(samples)
    bandpass_ampl = get_rms(bandpass_samples)
    #print(bandpass_ampl)
    print(amplitude)

    #data_int = struct.unpack(str(2*CHUNK) + 'B', data)
    #magnitude = np.convolve(data_int, filter.filter_1000)
    #sample_magnitude = np.sum(np.multiply(magnitude, magnitude))
    #data_np = np.array(data_int, dtype='b')[::2] + 128
    #y_fft = fft(data_int)
    #magnitude = np.abs(y_fft[0:CHUNK])*2/(256 *CHUNK)
    #subfrequencies = magnitude[100:500]
    #line_fft.set_ydata(magnitude)
    #ax_freq = np.argmax(subfrequencies)
    #print("value of difference: %d" % np.abs(np.argmax(magnitude) - np.argmin(magnitude)))
    #print("max freq occurs at: %f, %f" % ((max_freq + 100) * interval, subfrequencies[max_freq]))
    #fig.canvas.draw()
    #fig.canvas.flush_events()





