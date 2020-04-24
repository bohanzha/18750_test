import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft
from detector import InitialSequenceFsm, ThresholdDetector
import hamming
import pdb

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 2

#fig, (ax2) = plt.subplots(1, figsize=(15, 8))

x = np.arange(0, 2 * CHUNK, 2)

# space in between points represents RATE/CHUNK Hz = 21.53 Hz interval
x_fft = np.linspace(0, RATE, CHUNK)

#line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)
#ax2.set_xlim(20, RATE / 2)
plt.show(block=False)

LOW_FREQ = 50  # 50*21.53 = 1076 HZ
HI_FREQ = 200  # 200*21.53 = 4306  Hz

interval = RATE / CHUNK
FRAME_SIZE = 12

stream = mic.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)
sequence_fsm = InitialSequenceFsm()
threshold_detector = ThresholdDetector(1500, 2600, 0.3)
data_frame = [0 for i in range(FRAME_SIZE)]
idx = 0
FRAME_TIMEOUT = 100
frame_timeout = FRAME_TIMEOUT
while True:
    data = stream.read(CHUNK)
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)

    #data_np = np.array(data_int, dtype='b')[::2] + 128
    y_fft = fft(data_int)
    magnitude = np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK)

    subfrequencies = magnitude[LOW_FREQ:HI_FREQ]
    #pdb.set_trace()
    #line_fft.set_ydata(magnitude)
    max_freq = np.argmax(subfrequencies)
    #if subfrequencies[max_freq] >= 0.3:
        #print("%d, %f" % ((max_freq + LOW_FREQ)*interval, subfrequencies[max_freq]))
    detected_bit = threshold_detector.detect((max_freq + LOW_FREQ)*interval,
                                             subfrequencies[max_freq])
    if detected_bit != -1:
        frame_timeout = FRAME_TIMEOUT
        #print("detected bit %d", detected_bit)
        data_frame[idx] = detected_bit
        if idx == FRAME_SIZE - 1:
            recovered_df = hamming.recover_frame(data_frame)
            char_value = int(''.join([str(bit) for bit in recovered_df]),2)
            recovered = chr(char_value)
            print(recovered)
        idx = (idx + 1)%FRAME_SIZE
    #if len(data_frame) == FRAME_SIZE:
    frame_timeout = frame_timeout - 1
    if frame_timeout == 0:
        #drop frame
        idx = 0


    #print("max freq occurs at: %f, %f" % ((max_freq + 100) * interval, subfrequencies[max_freq]))
    #fig.canvas.draw()
    #fig.canvas.flush_events()
