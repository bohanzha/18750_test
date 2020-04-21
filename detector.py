# 1101 state machine for sequence detection
import numpy as np

S_0 = 0
S_1 = 1
S_2 = 2
S_3 = 3
S_4 = 4

states = {
    S_0: {
        0: S_0,
        1: S_1
    },
    S_1: {
        1: S_2,
        0: S_0
    },
    S_2: {
        1: S_0,
        0: S_3,
    },
    S_3: {
        1: S_4,
        0: S_0
    }
}


class InitialSequenceFsm:
    curr_state = S_0

    def __init__(self):
        self.curr_state = S_0

    def clear(self):
        self.curr_state = S_0

    def is_start(self, curr_bit):
        self.curr_state = states[self.curr_state][curr_bit]
        if self.curr_state == S_4:
            self.clear()
            return True
        return False


LOW = "low"
F1 = "f1"
F2 = "f2"

threshold_states = {
    LOW: {
        0: LOW,
        1: F1
    },
    F1: {
        0: LOW,
        1: F1,
        2: F2
    },
    F2: {
        0: LOW,
        1: F2
    }
}


class ThresholdDetector:
    f1 = 0
    f0 = 0
    prev_state = LOW
    curr_state = LOW
    threshold = 0.3
    debounce = 4

    def transition(self, freq, magnitude):
        bit = -1
        if self.debounce > 0:
            self.debounce = self.debounce - 1
        else:
            if self.f0 <= freq < self.f1 \
                    and magnitude >= self.threshold:
                if self.curr_state is LOW:
                    self.prev_state = LOW
                    self.curr_state = F1

                else:
                    self.prev_state = F1
            elif freq >= self.f1 \
                    and magnitude >= self.threshold:
                if self.curr_state is LOW:
                    self.curr_state = F2
                    self.prev_state = LOW
                else:
                    self.prev_state = F2
            else:
                if self.prev_state is F1:
                    bit = 0
                elif self.prev_state is F2:
                    bit = 1
                self.debounce = 4
                self.clear()
        return bit

    def __init__(self, f0, f1, threshold):
        self.f1 = 0
        self.f0 = 0
        self.low = 0
        self.curr_state = LOW
        self.prev_state = LOW
        self.f1 = f1
        self.f0 = f0
        self.threshold = threshold
        self.debounce = 0

    def clear(self):
        self.curr_state = LOW
        self.prev_state = LOW

    def detect(self, detected_freq, magnitude):
        return self.transition(detected_freq,
                               magnitude)
