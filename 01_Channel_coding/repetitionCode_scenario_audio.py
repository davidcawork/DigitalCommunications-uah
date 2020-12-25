#!/usr/bin/python3

from RepetitionEncoding.repetitionCode import RepetitionCode
from Channel.channel import Channel, randBits, getGood
import numpy as npy
import simpleaudio as sa
import random
import time


def prepareBitStreamFromWaW(wave_obj):
    """
    Function to prepare data into binary stream
    """
    bitsTx_stream = list()
    data_bin = [npy.binary_repr(dec, 16) for dec in npy.frombuffer(wave_obj.audio_data, dtype=npy.int16)]
    for dec in data_bin:
        for bit in dec:
            bitsTx_stream.append(int(bit))
    return bitsTx_stream


def scenario(n=3, prob=0.02):
    "Main method to simulate a noisy scenario using Repetition codes"

    # Stats vars
    start_time = time.time()

    # Scenario behaviour
    print("Simulating Repetition code scenario (Audio)...\n")
    wave_obj = sa.WaveObject.from_wave_file('data/brahms_mono.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()

    print("Settintg up data into binary stream... \n")
    bitsTx = prepareBitStreamFromWaW(wave_obj)

    print("Encoding binary stream...\n")
    code_Tx = RepetitionCode.repetitionEncoder(bitsTx, n)

    print("Tx encoded data (usually takes time)...\n")
    code_Rx = Channel(prob).run(code_Tx)

    print("Decode data (usually takes time)...\n")
    bitsRx = RepetitionCode.repetitionDecoder(code_Rx, n)

    wave_obj.audio_data = bitsRx.tobytes()
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(len(bitsTx)))
    print('[+] Errors: '+str(code_Tx.size - getGood(code_Tx, code_Rx)))
    print('[+] Fixed: '+str(code_Rx.size - getGood(code_Rx, npy.repeat(npy.array(bitsRx), n))))
    print('[+] Error probability (calculated): '+str((code_Tx.size - getGood(code_Tx, code_Rx))/code_Tx.size))


if __name__ == '__main__':
    scenario(n=3, prob=0.02)
