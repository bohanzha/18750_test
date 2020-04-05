hamming_init = [(1, 0), (2, 1), (4, 3), (8, 7)]

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def recover_frame(data_frame):
    hamming_init = [(1,0), (2,1), (4,3), (8,7)]
    results = [0,0,0,0]
    for idx, hamming_pair in enumerate(hamming_init):
        parity = 0
        begin_idx = hamming_pair[1]
        while begin_idx < len(data_frame):
            for i in range(hamming_pair[0]):
                if (begin_idx + i) < len(data_frame):
                    parity ^= data_frame[begin_idx + i]
                #skip
            begin_idx = begin_idx + 2 *hamming_pair[0]
        results[idx] = parity
    #apply the error correction
    error_bit = 0;
    for idx, parity in enumerate(results):
        error_bit = error_bit + results[idx] * ( 1 << idx )
    if error_bit > 0 and error_bit <= len(data_frame):
        data_frame[error_bit-1] ^= 1
    #recover the dataframe
    df = data_frame[2:3] + data_frame[4:7] + data_frame[8:12]
    return df

def generate_hamming_frame(char_byte):
    bf = bitfield(ord(char_byte))
    #left_pad
    bf = [0] * (8 - len(bf)) + bf
    hamming_frame = [0,0] + bf[0:1] + [0] + bf[1:4] + [0] + bf[4:8]
    #compute parity bits
    for idx, hamming_pair in enumerate(hamming_init):
        parity = 0
        begin_idx = hamming_pair[1]
        while begin_idx < len(hamming_frame):
            for i in range(hamming_pair[0]):
                if (begin_idx + i) < len(hamming_frame):
                    parity ^= hamming_frame[begin_idx + i]
                #skip
            begin_idx = begin_idx + 2 *hamming_pair[0]
        hamming_frame[hamming_pair[1]] = parity
    return hamming_frame

data_frame = [0,1,1,1,0,0,1,0,1,1,1,0]
frame = generate_hamming_frame('C')
#resistant to single bit error
frame[11] ^= 1
rframe = recover_frame(frame)
result = chr(int("".join(str(x) for x in rframe), 2))
print(result)



